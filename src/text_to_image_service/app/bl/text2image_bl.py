import json

from ..helper.mongo_db import MongoDBClient
from .queue.rabbitmq import RabbitMQ
from ..schemas.schemas import OperationErrorSchema, Text2ImageOperationSchema, ImagesSchema
from ..storage import util
from ..models.models import Text2ImageOperation, Text2ImageOperationImage, OperationErrors
from bson import ObjectId
from io import BytesIO
import requests
import gridfs
from flask_pymongo import PyMongo
from openai import OpenAI
from flask import current_app
from sqlalchemy.orm import joinedload
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbitmq_port = int(os.getenv('RABBITMQ_PORT', 5672))
rabbitmq_user = os.getenv('RABBITMQ_USER', 'guest')
rabbitmq_password = os.getenv('RABBITMQ_PASS', 'guest')
rabbitmq_queue_name = os.getenv('RMQ_QUEUE', 'text2image')
rabbitmq_n_queue_name = os.getenv(
    'RMQ_storyboard_QUEUE', 'text2image_notification')

text_to_image_queue = RabbitMQ(host=rabbitmq_host, port=rabbitmq_port,
                               user=rabbitmq_user, password=rabbitmq_password, queue_name=rabbitmq_queue_name)

text_to_image_n_queue = RabbitMQ(host=rabbitmq_host, port=rabbitmq_port,
                                 user=rabbitmq_user, password=rabbitmq_password, queue_name=rabbitmq_n_queue_name)


# mongo_image = PyMongo(
#     current_app,
#     uri=os.getenv('MONGODB_URI_DB')
# )
# fs_images = gridfs.GridFS(mongo_image.db)


uri, db_name = os.getenv('MONGODB_URI'), os.getenv('MONGODB_DB')
mongo_client = MongoDBClient(uri, db_name)

fs_images = mongo_client.fs_db


def generate_image(prompt, aspect_ratio):
    size = "1024x1024"
    if aspect_ratio == '16:9':
        size = "1792x1024"
    elif aspect_ratio == '9:16':
        size = "1024x1792"

    openai_key = os.getenv('OPENAI_SECRET_KEY')
    client = OpenAI(api_key=openai_key)

    response = client.images.generate(
        model="dall-e-3",
        quality="standard",
        prompt=prompt,
        size=size
    )

    return response.data[0].url


def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        raise Exception("faild to download image")


def create_storyboard_operation_images(images_data, reference, orginal_script, db_session):
    text2image_operation_schema = Text2ImageOperationSchema()
    text2image_operation_data = {
        'reference': reference,
        'script_text': orginal_script
    }

    errors = text2image_operation_schema.validate(text2image_operation_data)
    if errors:
        raise Exception(errors)
    text2image_operation = Text2ImageOperation(**text2image_operation_data)
    images_list = []
    db_session.add(text2image_operation)
    db_session.flush()
    images_id = []
    returned_data = {}
    media_folder = os.getenv('MEDIA_FOLDER')
    save_data = {
        'reference': reference,
        'media_folder': media_folder
    }

    try:
        text2image_operation_id = text2image_operation.id
        save_data['text2image_operation_id'] = text2image_operation_id
        for image_data in images_data:
            image_url = image_data['url']

            image_byte = download_image(image_url)

            save_data['order'] = image_data['order']
            save_data['image'] = image_byte

            url = util.save_image(
                save_data, db_or_folder=1)
            images_id.append(url)
            returned_data[image_data['order']] = str(url)
            image_db_data = {
                'text2image_operation_id': text2image_operation_id,
                'order': image_data['order'],
                'scene_text': image_data['prompt'],
                'url': str(url)

            }
            image_schema = ImagesSchema()
            errors = image_schema.validate(image_db_data)
            if errors:
                raise Exception(errors)
            image_db_data = Text2ImageOperationImage(**image_db_data)
            images_list.append(image_db_data)

        if images_list:
            db_session.bulk_save_objects(images_list)
        db_session.commit()
        return returned_data
    except Exception as e:
        if images_id:
            # delete images from MongoDB
            for fid in images_id:
                os.remove(fid)
        raise e


def generate_storyboards(data, db_session, for_consumer=False):
    """Generates storyboards using DALL·E based on the script and user preferences.

    Args:
        script (str): The generated script to base the storyboards on.
        storyboard_style (str): The style of the storyboard.
        detailed (bool): Whether the storyboard should be detailed.
        colored (bool): Whether the storyboard should be colored.

    Returns:
        list: URLs of the generated storyboard images or error message placeholders.
    """
    # storyboards stylse, size, and other data
    try:
        if for_consumer:
            data = json.loads(data)
        orginal_script = data['orginal_script']
        prompts = data['prompts']
        reference = data['reference']
        aspect_ratio = data['aspect_ratio']
        storyboard_style = data['storyboard_style']
        prompt = ""
        images_data = []
        # prompt = f"I will give you the totla script, and the prompt of each image inside that script,"\
        #     "and you will generate an image for each prompt, and return list of images urls in the same order of the images prompts.\n"\
        #     f" all images should be {color_description}, and {detail_description}, and in the style of {storyboard_style}.\n"\
        #     f"the total script: {orginal_script} \n"\
        #     "the prompts are dictionary in this shape {\"image_order\":\"image_description\"}: "\
        #     f"{prompts}\n"\
        #     "return me list of urls in the same images' order"

        for key, value in prompts.items():
            prompt = f" Create image with aspect ratio: {aspect_ratio} for scene in the style of {storyboard_style} based on this description:{value}.\n"\
                " and take the total script of all scenes in considration to keep same context\n"\
                f"the total script: {orginal_script} \n"

            image_url = generate_image(prompt, aspect_ratio)
            image_data = {'order': key, 'prompt': prompt, 'url': image_url}

            images_data.append(image_data)
        returned_data = create_storyboard_operation_images(
            images_data, reference, orginal_script, db_session)
        if for_consumer:
            # send message to text_to_message_notification
            set_message_storyboards_images(reference, returned_data)
            return
        return {'data': images_data, }
    except Exception as e:
        if for_consumer:
            # insert in error table
            error_processing(reference, str(e.args), prompt, db_session)
            return
        else:
            raise e


def insert_error(reference, error, message, db_session):
    operation_error_schema = OperationErrorSchema()
    operation_error_data = {
        'reference': reference,
        'script_text': message,
        "error": error
    }

    errors = operation_error_schema.validate(operation_error_data)
    if errors:
        raise Exception(errors)
    operation_error = OperationErrors(**operation_error_data)
    db_session.add(operation_error)
    db_session.commit()


def error_processing(reference, error, message, db_session):
    try:
        insert_error(reference, error, message, db_session)
        set_message_storyboards_images(
            reference, dict_data=None, success=0, e_message=error)
    except Exception as e:
        pass


def set_message_storyboards_images(reference, dict_data=None, success=1, e_message=None):
    message = {
        'success': success,
        'e_message': e_message,
        'reference': reference,
        'images_data': dict_data}
    text_to_image_n_queue.send_message(
        routing_key=rabbitmq_n_queue_name, message=message)


def get_images_id(ref_id, db_session):
    t2m_op = Text2ImageOperation.query.filter_by(reference=ref_id).first()
    images = db_session.query(Text2ImageOperationImage).filter_by(
        text2image_operation_id=t2m_op.id).order_by(Text2ImageOperationImage.order).all()
    images_id = [im.url for im in images]
    images_data = []
    for file_id in images_id:
        try:
            file_data = fs_images.get(ObjectId(file_id))
            image = {
                'id': file_id,
                'filename': file_data.filename,
                'content': file_data.read()
            }
            images_data.append(image)
        except gridfs.errors.NoFile:
            images_data.append({'id': file_id, 'content': None})
    return images_data


def consumer_bl(db_session):
    try:
        callback_func = text_to_image_queue.create_callback(
            generate_storyboards, db_session)
        text_to_image_queue.consumer(
            queue=rabbitmq_queue_name, callback=callback_func)
    except Exception as e:
        print(f"An error occurred: {e}")
        db_session.rollback()
    finally:
        db_session.close()

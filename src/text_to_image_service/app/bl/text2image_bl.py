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

text_to_image_queue = RabbitMQ(
    host=rabbitmq_host, port=rabbitmq_port, user=rabbitmq_user, password=rabbitmq_password)

# mongo_image = PyMongo(
#     current_app,
#     uri=os.getenv('MONGODB_URI_DB')
# )
# fs_images = gridfs.GridFS(mongo_image.db)


uri, db_name = os.getenv('MONGODB_URI'), os.getenv('MONGODB_DB')
mongo_client = MongoDBClient(uri, db_name)

fs_images = mongo_client.fs_db


def generate_image(prompt):
    openai_key = os.getenv('OPENAI_SECRET_KEY')
    client = OpenAI(api_key=openai_key)

    response = client.images.generate(
        model="dall-e-3",
        size="1024x1024",
        quality="standard",
        prompt=prompt

    )

    return response.data[0].url


def download_image(url):
    response = requests.get(url)
    return BytesIO(response.content)


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
    try:
        text2image_operation_id = text2image_operation.id
        for image_data in images_data:
            image_url = image_data['url']
            image_byte = download_image(image_url)
            url = util.save_to_db(image_byte, image_data['order'], fs_images)
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
                fs_images.delete(fid)
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
        color_description = data['color_description']
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
            prompt = f"I will give you the total script, and the prompt of the image inside that script,"\
                f"the total script: {orginal_script} \n"\
                f" Create a {color_description}, {aspect_ratio} storyboard in the style of {storyboard_style} based on this storyboard description:{value}.\n"\

            image_url = generate_image(prompt)
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
    except Exception as e:
        pass


def set_message_storyboards_images(reference, dict_data):
    message = {'reference': reference,
               'images_data': dict_data}
    text_to_image_queue.send_message(routing_key=os.getenv(
        'RMQ_storyboard_QUEUE'), message=message)


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
        text_to_image_queue.consumer(queue=os.getenv(
            'RMQ_QUEUE'), callback=callback_func)
    except Exception as e:
        print(f"An error occurred: {e}")
        db_session.rollback()
    finally:
        db_session.close()

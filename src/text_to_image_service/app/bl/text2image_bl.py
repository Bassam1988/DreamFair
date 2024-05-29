import ast
import json
from sqlalchemy.orm import joinedload
from flask import current_app
from openai import OpenAI
from flask_pymongo import PyMongo
import gridfs
import requests
from io import BytesIO
from bson import ObjectId

from ..models.models import Text2ImageOperation, Text2ImageOperationImage

from ..storage import util

from ..schemas.schemas import Text2ImageOperationSchema, ImagesSchema
from ..database import db_session

mongo_image = PyMongo(
    current_app,
    uri=current_app.config.get('MONGODB_URI')
)
fs_images = gridfs.GridFS(mongo_image.db)


def generate_image(prompt):
    openai_key = current_app.config.get('OPENAI_KEY')
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


def create_storyboard_operation_images(images_data, reference, orginal_script):
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
    try:
        text2image_operation_id = text2image_operation.id
        for image_data in images_data:
            image_url = image_data['url']
            image_byte = download_image(image_url)
            url = util.save_to_db(image_byte, image_data['order'], fs_images)
            images_id.append(url)
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
        return images_id
    except Exception as e:
        if images_id:
            # delete images from MongoDB
            for fid in images_id:
                fs_images.delete(fid)
        raise e


def generate_storyboards(data):
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
    orginal_script = data['script']
    prompts = data['prompts']
    reference = data['reference']
    detail_description = data['detail_description']
    color_description = data['color_description']
    storyboard_style = 'Sketch/Doodly'

    images_data = []
    # prompt = f"I will give you the totla script, and the prompt of each image inside that script,"\
    #     "and you will generate an image for each prompt, and return list of images urls in the same order of the images prompts.\n"\
    #     f" all images should be {color_description}, and {detail_description}, and in the style of {storyboard_style}.\n"\
    #     f"the total script: {orginal_script} \n"\
    #     "the prompts are dictionary in this shape {\"image_order\":\"image_description\"}: "\
    #     f"{prompts}\n"\
    #     "return me list of urls in the same images' order"

    for key, value in prompts.items():
        prompt = f"I will give you the totla script, and the prompt of the image inside that script,"\
            f"the total script: {orginal_script} \n"\
            f" Create a {color_description}, {detail_description} storyboard in the style of {storyboard_style} based on this storyboard description:{value}.\n"\

        image_url = generate_image(prompt)
        image_data = {'order': key, 'prompt': prompt, 'url': image_url}

        images_data.append(image_data)
    create_storyboard_operation_images(images_data, reference, orginal_script)

    return {'data': images_data, }


def get_images_id(ref_id):
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

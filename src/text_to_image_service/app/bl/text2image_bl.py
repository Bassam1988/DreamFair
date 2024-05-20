import ast
import json
from sqlalchemy.orm import joinedload
from flask import current_app
from openai import OpenAI

from ..models.models import Text2TextOperation, Text2TextOperationStoryboard


from ..schemas.schemas import StoryboardSchema, Text2TextOperationSchema
from ..database import db_session


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
    # prompts = data['prompts']
    prompts = data['prompts']
    detail_description = data['detail_description']
    color_description = data['color_description']
    storyboard_style = 'Sketch/Doodly'

    openai_key = current_app.config.get('OPENAI_KEY')
    client = OpenAI(api_key=openai_key)

    images_urls = []
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

        try:
            response = client.images.generate(
                model="dall-e-3",
                size="1024x1024",
                quality="standard",
                prompt=prompt

            )

            images_urls.append(response.data[0].url)

        except Exception as e:
            images_urls.append("img.png")

    return {'data': images_urls, }

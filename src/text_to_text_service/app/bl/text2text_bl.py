import ast
import json
from sqlalchemy.orm import joinedload
from flask import current_app
from openai import OpenAI


from ..schemas.schemas import AspectRatioSchema, BoardsPerMinSchema, ProjectSchema, ScriptStyleSchema, StoryBoardStyleSchema, StoryboardSchema, VideoDurationSchema
from ..database import db_session


def create_operation_storyboard(dict_data, response_data_message):
    if dict_data:
        pass


def generate_script(data):
    """Generates a script using OpenAI based on user inputs.

    Args:
        synopsis (str): User-provided synopsis for the script.
        script_style (str): The desired style of the script.
        video_duration (str): The desired duration of the video.

    Returns:
        str: The generated script or an error message.
    """
    synopsis = data['synopsis']
    script_style = data['script_style']
    video_duration = data['video_duration']
    openai_key = current_app.config.get('OPENAI_KEY')
    client = OpenAI(api_key=openai_key)
    prompt = f"Generate a script in the style of {script_style} for a video lasting {video_duration},\
          inspired by the following synopsis: {synopsis}.\
              After generating the script write the storyboards as image or "\
                "storyboard descriptions as dictionary with the following annotation: "\
        "Image Number: generated storyboard description. "\
        "add the hole result as dictionary, like this:"\
        "{'script': 'the generated script', 'storyboards':{'1':'generated storyboard 1','2':'generated storyboard 2', ...}} "\
        " and without any additional characters "\
        "don't add \n at the end of result, the result should begine and end like this {} "\
        "don't add \n out side the generated text, the result should be exactly like this"\
        "'{\"script\":\"generated script\",\"storyboards\":{\"1\":\"generated storyboard 1\",\"2\":\"generated storyboard 2\", ...}}' "
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a senior scripts writer and artist."},
                {"role": "user", "content": prompt}
            ]
        )
        response_data_message = str(
            response.choices[0].message.content)
        dict_data = None
        try:
            dict_data = ast.literal_eval(response_data_message)
        except:
            try:
                dict_data = json.loads(response_data_message)
            except Exception as e:
                raise e

        create_operation_storyboard(dict_data, response_data_message)
        response_data = {'data': dict_data}

        return response_data
    except Exception as e:
        return "Failed to generate script."

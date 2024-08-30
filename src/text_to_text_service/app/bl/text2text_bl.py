import json
import ast
from openai import OpenAI
from .queue.rabbitmq import RabbitMQ
from ..models.models import OperationErrors, Text2TextOperation, Text2TextOperationStoryboard
from ..schemas.schemas import OperationErrorSchema, StoryboardSchema, Text2TextOperationSchema
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbitmq_port = int(os.getenv('RABBITMQ_PORT', 5672))
rabbitmq_user = os.getenv('RABBITMQ_USER', 'guest')
rabbitmq_password = os.getenv('RABBITMQ_PASS', 'guest')
rabbitmq_queue_name = os.getenv('RMQ_QUEUE', 'tex2text')
rabbitmq_n_queue_name = os.getenv(
    'RMQ_storyboard_QUEUE', 'text2text_notification')

text_to_text_queue = RabbitMQ(host=rabbitmq_host, port=rabbitmq_port,
                              user=rabbitmq_user, password=rabbitmq_password, queue_name=rabbitmq_queue_name)

text_to_text_n_queue = RabbitMQ(host=rabbitmq_host, port=rabbitmq_port,
                                user=rabbitmq_user, password=rabbitmq_password, queue_name=rabbitmq_n_queue_name)


def create_operation_storyboard(dict_data, response_data_message, reference, prompt, db_session):
    text2text_operation_schema = Text2TextOperationSchema()
    text2text_operation_data = {
        'reference': reference,
        'original_text': prompt,
        'generated_text': response_data_message}

    generated_script = ""
    if dict_data:
        generated_script = dict_data['script']
    text2text_operation_data['generated_script'] = generated_script
    errors = text2text_operation_schema.validate(text2text_operation_data)
    if errors:
        raise Exception(errors)
    text2text_operation = Text2TextOperation(**text2text_operation_data)
    storyboards_list = []
    db_session.add(text2text_operation)
    db_session.flush()
    if dict_data:
        text2text_operation_id = text2text_operation.id
        storyboards = dict_data['storyboards']
        for key, value in storyboards.items():
            storyboard_data = {
                'text2text_operation_id': text2text_operation_id,
                'order': key,
                'generated_text': value
            }
            storyboard_schema = StoryboardSchema()
            errors = storyboard_schema.validate(storyboard_data)
            if errors:
                raise Exception(errors)
            storyboard = Text2TextOperationStoryboard(**storyboard_data)
            storyboards_list.append(storyboard)

    if storyboards_list:
        db_session.bulk_save_objects(storyboards_list)
    db_session.commit()


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
        set_message_storyboards(
            reference, dict_data=None, success=0, error=error)
    except Exception as e:
        pass


def generate_script(data, db_session, for_consumer=False):
    """Generates a script using OpenAI based on user inputs.

    Args:
        synopsis (str): User-provided synopsis for the script.
        script_style (str): The desired style of the script.
        video_duration (str): The desired duration of the video.

    Returns:
        str: The generated script or an error message.
    """
    if for_consumer:
        data = json.loads(data)
    synopsis = data['synopsis']
    script_style = data['script_style']
    video_duration = data['video_duration']
    reference = data.get('reference', None)
    openai_key = os.getenv('OPENAI_SECRET_KEY')

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
            model="gpt-4o",
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

        create_operation_storyboard(
            dict_data, response_data_message, reference, prompt, db_session)
        response_data = {'data': dict_data}
        if for_consumer:
            # insert result in text2text_notification queue to get it to storyboard app
            set_message_storyboards(reference=reference, dict_data=dict_data)
            return
        return response_data
    except Exception as e:
        if for_consumer:
            # insert in error table
            error_processing(reference, str(e.args), prompt, db_session)
            return
        else:
            raise e


def set_message_storyboards(reference, dict_data=None, success=1, error=None):
    dict_data['reference'] = reference
    dict_data['success'] = success
    dict_data['e_message'] = error
    text_to_text_n_queue.send_message(
        routing_key=rabbitmq_n_queue_name, message=dict_data)


def consumer_bl(db_session):
    try:
        callback_func = text_to_text_queue.create_callback(
            generate_script, db_session)
        text_to_text_queue.consumer(
            queue=rabbitmq_queue_name, callback=callback_func)
    except Exception as e:
        print(f"An error occurred: {e}")
        db_session.rollback()
    finally:
        db_session.close()

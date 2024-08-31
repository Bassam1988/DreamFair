import json
from ..database import db_session
from ..schemas.schemas import AspectRatioSchema, BoardsPerMinSchema, ProjectSchema, ScriptStyleSchema, StoryBoardStyleSchema, StoryboardSchema, T2IOperationErrorSchema, T2TOperationErrorSchema, VideoDurationSchema
from ..models.models import AspectRatio, BoardsPerMin, Project, ScriptStyle, Status, StoryBoardStyle, Storyboard, T2IOperationErrors, T2TOperationErrors, VideoDuration
from .queue.rabbitmq import RabbitMQ
from sqlalchemy.orm import joinedload
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbitmq_port = int(os.getenv('RABBITMQ_PORT', 5672))
rabbitmq_user = os.getenv('RABBITMQ_USER', 'guest')
rabbitmq_password = os.getenv('RABBITMQ_PASS', 'guest')
t_n_queue = os.getenv('RMQ_T2T_N_QUEUE')
m_n_queue = os.getenv('RMQ_T2M_N_QUEUE')

t_queue = os.getenv('RMQ_QUEUE')
m_queue = os.getenv('RMQ_IMAGE_QUEUE')

text_to_text_n_queue = RabbitMQ(
    host=rabbitmq_host, port=rabbitmq_port, user=rabbitmq_user, password=rabbitmq_password, queue_name=t_n_queue)

text_to_image_n_queue = RabbitMQ(
    host=rabbitmq_host, port=rabbitmq_port, user=rabbitmq_user, password=rabbitmq_password, queue_name=m_n_queue)


text_to_text_queue = RabbitMQ(
    host=rabbitmq_host, port=rabbitmq_port, user=rabbitmq_user, password=rabbitmq_password, queue_name=t_queue)

text_to_image_queue = RabbitMQ(
    host=rabbitmq_host, port=rabbitmq_port, user=rabbitmq_user, password=rabbitmq_password, queue_name=m_queue)


def get_all_projects(user_id):
    project_schema = ProjectSchema()
    projects = Project.query.filter_by(user_id=user_id).all()
    data = project_schema.dump(projects, many=True)
    return {'data': data, 'status': 200}


def get_project_by_id(user_id, project_id):
    project_schema = ProjectSchema()
    project = Project.query.get(project_id)
    if project and str(project.user_id) == user_id:
        project.storyboards = db_session.query(Storyboard).filter(
            Storyboard.project_id == project.id
        ).order_by(Storyboard.order).all()
        data = project_schema.dump(project)
        return {'data': data, 'status': 200}
    return {'message': 'No data found', 'status': 404}


def create_project_bl(data, user_id):
    project_schema = ProjectSchema()
    errors = project_schema.validate(data)
    if errors:
        return {'errors': errors, 'status': 400}
    project = Project(
        user_id=user_id,
        name=data['name'],
        synopsis=data['synopsis'],
        script=data.get('script', None),
        status=Status.query.filter(Status.code_name == 'Wa').first(),
        script_style_id=data.get('script_style_id', None),
        storyboard_style_id=data.get('storyboard_style_id', None),
        video_duration_id=data.get('video_duration_id', None),
        aspect_ratio_id=data.get('aspect_ratio_id', None),
        boards_per_min_id=data.get('boards_per_min_id', None)
    )

    db_session.add(project)
    db_session.commit()
    return {'data': {'project': project_schema.dump(project)}, 'safe': False, 'status': 201}


def update_project_by_id(user_id, project_id, update_data):
    project = Project.query.get(project_id)
    if project and str(project.user_id) == user_id:
        for key, value in update_data.items():
            setattr(project, key, value)

        db_session.commit()
        project_schema = ProjectSchema()
        data = project_schema.dump(project)
        return {'data': data, 'status': 200}
    return {'message': 'No data found', 'status': 404}


def get_all_script_styles():
    script_style_schema = ScriptStyleSchema()
    script_styles = ScriptStyle.query.all()
    data = script_style_schema.dump(script_styles, many=True)
    return {'data': data, 'message': '', 'status': 200}


def get_all_storyboard_styles():
    storyboard_style_schema = StoryBoardStyleSchema()
    storyboard_styles = StoryBoardStyle.query.all()
    data = storyboard_style_schema.dump(storyboard_styles, many=True)
    return {'data': data, 'status': 200}


def get_all_video_durations():
    video_duration_schema = VideoDurationSchema()
    video_durations = VideoDuration.query.all()
    data = video_duration_schema.dump(video_durations, many=True)
    return {'data': data, 'status': 200}


def get_all_aspect_ratios():
    aspect_ratio_schema = AspectRatioSchema()
    aspect_ratios = AspectRatio.query.all()
    data = aspect_ratio_schema.dump(aspect_ratios, many=True)
    return {'data': data, 'status': 200}


def get_all_boards_per_mins():
    boards_per_min_schema = BoardsPerMinSchema()
    boards_per_mins = BoardsPerMin.query.all()
    data = boards_per_min_schema.dump(boards_per_mins, many=True)
    return {'data': data, 'status': 200}


def get_project_storyboard_bl(user_id, project_id):
    project_storyboard_schema = StoryboardSchema()
    project_storyboards = db_session.query(Storyboard).join(Project).\
        filter(Storyboard.project_id == project_id, Project.user_id == user_id).\
        options(joinedload(Storyboard.project)).all()
    if project_storyboards:
        data = project_storyboard_schema.dump(project_storyboards, many=True)
        return {'data': data, 'status': 200}
    return {'message': 'No data found', 'status': 404}


def send_synopsis(user_id, project_id):
    project_schema = ProjectSchema()
    project = Project.query.get(project_id)
    if project and str(project.user_id) == user_id:
        synopsis = project.synopsis
        reference = str(project.id)
        script_style = project.script_style
        if script_style:
            script_style_name = script_style.name
        else:
            return {'message': 'Script Style is mandatory', 'status': 400}

        video_duration = project.video_duration
        if video_duration:
            video_duration_name = video_duration.name
        else:
            return {'message': 'Video duration is mandatory', 'status': 400}
        message = {
            "reference": reference,
            "synopsis": synopsis,
            "script_style": script_style_name,
            "video_duration": video_duration_name,
        }
        text_to_text_queue.send_message(
            message=message, routing_key=t_queue)
        project.status = Status.query.filter(
            Status.code_name == 'GeSc').first()
        db_session.commit()
        data = project_schema.dump(project)
        return {'data': data, 'status': 200}
    return {'message': 'No data found', 'status': 404}


def send_script(user_id, project_id):
    project_schema = ProjectSchema()
    project = Project.query.get(project_id)
    if project and str(project.user_id) == user_id:

        reference = str(project.id)

        orginal_script = project.script

        prompts = {prompt.order: prompt.scene_description
                   for prompt in project.storyboards}

        aspect_ratio = project.aspect_ratio
        if aspect_ratio:
            aspect_ratio_name = aspect_ratio.name
        else:
            return {'message': 'Aspect ratio is mandatory', 'status': 400}

        boards_per_min = project.boards_per_min
        if boards_per_min:
            boards_per_min_count = boards_per_min.count
        else:
            return {'message': 'Boards per min is mandatory', 'status': 400}

        storyboard_style = project.storyboard_style
        if storyboard_style:
            storyboard_style_name = storyboard_style.name
        else:
            return {'message': 'Storyboard tyle is mandatory', 'status': 400}

        message = {
            "reference": reference,
            "orginal_script": orginal_script,
            "prompts": prompts,
            "aspect_ratio": aspect_ratio_name,
            "storyboard_style": storyboard_style_name,
        }
        text_to_image_queue.send_message(
            message=message, routing_key=m_queue)
        project.status = Status.query.filter(
            Status.code_name == 'GeSt').first()
        db_session.commit()
        data = project_schema.dump(project)
        return {'data': data, 'status': 200}
    return {'message': 'No data found', 'status': 404}


def t2t_insert_error(reference, error, message, db_session):
    operation_error_schema = T2TOperationErrorSchema()
    operation_error_data = {
        'reference': reference,
        'script_text': message,
        "error": error
    }
    errors = operation_error_schema.validate(operation_error_data)
    if errors:
        raise Exception(errors)
    operation_error = T2TOperationErrors(**operation_error_data)
    db_session.add(operation_error)
    db_session.commit()


def t2t_error_processing(reference, error, message, db_session):
    try:
        t2t_insert_error(reference, error, message, db_session)
    except Exception as e:
        pass


def set_scribt_storyboard_desc(data, db_session, for_consumer=True):
    try:
        dict_data = json.loads(data)
        storyboards_list = []
        project_id = dict_data['reference']
        project = Project.query.get(project_id)
        success = dict_data['success']
        if project:
            if success == 1:
                db_session.query(Storyboard).filter(
                    Storyboard.project_id == project.id).delete()
                storyboards = dict_data['storyboards']
                project_script = dict_data['script']
                project.script = project_script
                for key, value in storyboards.items():
                    storyboard_data = {
                        'project_id': project.id,
                        'order': key,
                        'scene_description': value,
                        'name': key
                    }
                    storyboard_schema = StoryboardSchema()
                    errors = storyboard_schema.validate(storyboard_data)
                    if errors:
                        raise Exception(errors)
                    storyboard = Storyboard(**storyboard_data)
                    storyboards_list.append(storyboard)

                if storyboards_list:
                    db_session.bulk_save_objects(storyboards_list)
                project.status = Status.query.filter(
                    Status.code_name == 'GedSc').first()
                db_session.commit()
                return
            else:
                project.status = Status.query.filter(
                    Status.code_name == 'Wa').first()
                db_session.commit()
                error = dict_data['e_message']
                raise error
        return "error"
    except Exception as e:
        if for_consumer:
            # insert in error table
            t2t_error_processing(project_id, str(e),
                                 project_script, db_session)
            return
        else:
            raise e


def t2i_insert_error(reference, error, message, db_session):
    operation_error_schema = T2IOperationErrorSchema()
    operation_error_data = {
        'reference': reference,
        'script_text': message,
        "error": error
    }
    errors = operation_error_schema.validate(operation_error_data)
    if errors:
        raise Exception(errors)
    operation_error = T2IOperationErrors(**operation_error_data)
    db_session.add(operation_error)
    db_session.commit()


def t2i_error_processing(reference, error, message, db_session):
    try:
        t2i_insert_error(reference, error, message, db_session)
    except Exception as e:
        pass


def set_scribt_storyboard_images(data, db_session, for_consumer=True):
    try:
        dict_data = json.loads(data)

        project_id = dict_data['reference']
        project = Project.query.get(project_id)
        success = dict_data['success']
        if project:
            if success == 1:

                images_data = dict_data['images_data']
                storyboards = db_session.query(Storyboard).filter_by(
                    project_id=project.id).order_by(Storyboard.order).all()
                for storyboard in storyboards:
                    storyboard.image = images_data[str(storyboard.order)]

                project.status = Status.query.filter(
                    Status.code_name == 'GedSt').first()
                db_session.commit()
                return
            else:
                project.status = Status.query.filter(
                    Status.code_name == 'GedSc').first()
                db_session.commit()
                error = dict_data['e_message']
                raise error
        return "error"
    except Exception as e:
        if for_consumer:
            # insert in error table
            t2i_error_processing(project_id, str(e),
                                 str(images_data), db_session)
            return
        else:
            raise e


def t2t_consumer_bl(db_session):
    try:
        callback_func = text_to_text_n_queue.create_callback(
            set_scribt_storyboard_desc, db_session)
        text_to_text_n_queue.consumer(queue=os.getenv(
            'RMQ_T2T_N_QUEUE'), callback=callback_func)
    except Exception as e:
        print(f"An error occurred: {e}")
        db_session.rollback()
    finally:
        db_session.close()


def t2m_consumer_bl(db_session):
    try:
        callback_func = text_to_image_n_queue.create_callback(
            set_scribt_storyboard_images, db_session)
        text_to_image_n_queue.consumer(queue=os.getenv(
            'RMQ_T2M_N_QUEUE'), callback=callback_func)
    except Exception as e:
        print(f"An error occurred: {e}")
        db_session.rollback()
    finally:
        db_session.close()

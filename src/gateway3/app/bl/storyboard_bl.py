import json
from sqlalchemy.orm import joinedload
from dotenv import load_dotenv
import os

from ..storyboard_svc.storyboard import get_storyboard_user_project

# Load environment variables from .env file
load_dotenv()


def get_all_projects(user_id):

    projects = get_storyboard_user_project(user_id)

    return {'data': projects, 'status': 200}


def get_project_by_id(user_id, project_id):
    project_schema = ProjectSchema()
    project = Project.query.get(project_id)
    if project and str(project.user_id) == user_id:
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
        script=data['script'],
        script_style_id=data['script_style_id'],
        storyboard_style_id=data['storyboard_style_id'],
        video_duration_id=data['video_duration_id'],
        aspect_ratio_id=data['aspect_ratio_id'],
        boards_per_min_id=data['boards_per_min_id']
    )

    db_session.add(project)
    db_session.commit()
    return {'data': {'project': project_schema.dump(project)}, 'safe': False, 'status': 201}


def get_all_script_styles():
    script_style_schema = ScriptStyleSchema()
    script_styles = ScriptStyle.query.all()
    data = script_style_schema.dump(script_styles, many=True)
    return {'data': data, 'status': 200}


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
        script_style = project.script_style.name
        video_duration = project.video_duration.name
        message = {
            "reference": reference,
            "synopsis": synopsis,
            "script_style": script_style,
            "video_duration": video_duration,
        }
        text_to_text_queue.send_message(
            message=message, routing_key=os.getenv('RMQ_QUEUE'))
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

        aspect_ratio = project.aspect_ratio.name
        boards_per_min = project.boards_per_min.count
        storyboard_style = project.storyboard_style.name

        message = {
            "reference": reference,
            "orginal_script": orginal_script,
            "prompts": prompts,
            "aspect_ratio": aspect_ratio,
            "color_description": boards_per_min,
            "storyboard_style": storyboard_style,
        }
        text_to_text_queue.send_message(
            message=message, routing_key=os.getenv('RMQ_IMAGE_QUEUE'))
        data = project_schema.dump(project)
        return {'data': data, 'status': 200}
    return {'message': 'No data found', 'status': 404}


def set_scribt_storyboard_desc(data, db_session, for_consumer=True):
    dict_data = json.loads(data)
    storyboards_list = []
    project_id = dict_data['reference']
    project = Project.query.get(project_id)
    if project:
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
        db_session.commit()
        return
    return "error"


def set_scribt_storyboard_images(data, db_session, for_consumer=True):
    dict_data = json.loads(data)

    project_id = dict_data['reference']
    project = Project.query.get(project_id)
    if project:
        images_data = dict_data['images_data']
        storyboards = db_session.query(Storyboard).filter_by(
            project_id=project.id).order_by(Storyboard.order).all()
        for storyboard in storyboards:
            storyboard.image = images_data[str(storyboard.order)]
        db_session.commit()
        return
    return "error"
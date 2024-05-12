from sqlalchemy.orm import joinedload
from flask import current_app

from ..models.models import AspectRatio, BoardsPerMin, Project, ScriptStyle, StoryBoardStyle, Storyboard, VideoDuration
from ..schemas.schemas import AspectRatioSchema, BoardsPerMinSchema, ProjectSchema, ScriptStyleSchema, StoryBoardStyleSchema, StoryboardSchema, VideoDurationSchema
from ..database import db_session


import json
import requests


def token_required_bl(token):

    response = requests.get(
        f"{current_app.config.get('AUTH_SVC_ADDRESS')}/token/validate",
        headers={"Authorization": token},
    )

    if response.status_code == 200:
        response_data = json.loads(response.text)
        user_data = response_data.get('data', {}).get('user', {})
        return {'current_user': user_data, 'message': '', 'status': 200}
    else:
        return {'message': response.text, 'status': response.status_code}


def get_all_projects(user_id):
    project_schema = ProjectSchema()
    projects = Project.query.filter_by(user_id=user_id).all()
    data = project_schema.dump(projects, many=True)
    return {'data': data, 'status': 200}


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

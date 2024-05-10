from sqlalchemy.orm import joinedload
import jwt

from ..models.models import Project
from ..schemas.schemas import ProjectSchema
from ..database import db_session
from flask import current_app

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
    projects = Project.query.filter_by(user_id=user_id).options(
        joinedload(Project.script_style)).all()
    data = project_schema.dump(projects, many=True)
    return {'data': data, 'status': 200}


def get_project_by_id(user_id, project_id):
    project_schema = ProjectSchema()
    project = Project.query.options(
        joinedload(Project.script_style)).get(project_id)
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

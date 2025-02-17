import shutil
import copy
import json

from ..schemas.history_schemas import ProjectHistoryListSchema, ProjectHistorySchema, StoryboardHistoryCreateSchema
from ..database import db_session
from ..schemas.schemas import AspectRatioSchema, BoardsPerMinSchema, ProjectSchema, ScriptStyleSchema, StoryBoardStyleSchema, StoryboardSchema, T2IOperationErrorSchema, T2TOperationErrorSchema, VideoDurationSchema
from ..models.models import AspectRatio, BoardsPerMin, Project, ProjectHistory, ScriptStyle, Status, StoryBoardStyle, Storyboard, StoryboardHistory, T2IOperationErrors, T2TOperationErrors, VideoDuration
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
    projects = Project.query.filter_by(user_id=user_id).order_by(
        Project.created_date.desc()).all()
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


def get_all_project_histories(user_id, project_id):
    project_history_schema = ProjectHistoryListSchema()

    project_histories = db_session.query(ProjectHistory).join(Project).\
        filter(ProjectHistory.project_id == project_id, Project.user_id == user_id).\
        options(joinedload(ProjectHistory.project)).order_by(
        ProjectHistory.created_date.desc()).all()

    data = project_history_schema.dump(project_histories, many=True)
    return {'data': data, 'status': 200}


def get_project_h_by_id(user_id, project_h_id):
    project_h_schema = ProjectHistorySchema()
    project_h = ProjectHistory.query.get(project_h_id)
    if project_h and str(project_h.project.user_id) == user_id:
        project_h.storyboards_history = db_session.query(StoryboardHistory).filter(
            StoryboardHistory.projects_history_id == project_h.id
        ).order_by(StoryboardHistory.order).all()
        data = project_h_schema.dump(project_h)
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
        synopsis=data.get('synopsis', None),
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


def revert_moved_images(moved_paths):
    """
    moved_paths is a list of tuples: [(original_path, new_path), ...]
    Move each file back from new_path to original_path.
    Ignore FileNotFoundError (already missing).
    """
    # It's often safer to revert in reverse order (last moved -> first undone).
    # But if order doesn't matter for your scenario, a normal loop is also fine.
    for original_path, new_path in reversed(moved_paths):
        if new_path and original_path:
            try:
                shutil.move(new_path, original_path)
            except FileNotFoundError:
                # If it's missing, skip silently or log it
                print(f"Revert warning: {new_path} not found.")
            except Exception as e:
                print(f"Error reverting {new_path} -> {original_path}: {e}")


def move_image_to_history_folder(old_image_path, p_h_id):
    """
    Move an image file from its current folder into a `history` subfolder 
    located in the same parent directory. For example:

        If old_image_path = "/images/projects/0021/img1.jpg",
        then new_image_path = "/images/projects/0021/history/img1.jpg".

    Returns the new image path.
    """
    if not old_image_path:
        return None

    # Extract the directory and filename
    # e.g. ("/images/projects/0021", "img1.jpg")
    directory, filename = os.path.split(old_image_path)

    # Create the 'history' subfolder if it does not exist
    # e.g. "/images/projects/0021/history"
    history_folder = os.path.join(directory, "history", str(p_h_id))
    if not os.path.exists(history_folder):
        os.makedirs(history_folder)

    # Build the new path inside the 'history' folder
    new_image_path = os.path.join(history_folder, filename)

    # Move the file
    try:
        shutil.move(old_image_path, new_image_path)
    except FileNotFoundError:
        # If the file doesn't exist, decide how you want to handle it
        # (e.g., log a warning, raise an exception, skip quietly, etc.)
        print(f"Warning: File not found: {old_image_path}")
        return None

    return new_image_path


def create_storyboard_history(project_h_id, project_storyboards):
    project_storyboard_schema = StoryboardHistoryCreateSchema()

    history_data = []
    pathes = []
    try:
        data = project_storyboard_schema.dump(
            project_storyboards, many=True)
        for item in data:
            # new_path = move_image_to_history_folder(
            #     item["image"], project_h_id)
            # pathes.append((new_path, item["image"]))
            history_data.append(
                {
                    "name": item["name"],
                    "image": item["image"],
                    "order": item["order"],
                    "scene_description": item["scene_description"],
                    "projects_history_id": project_h_id,

                }

            )

    # Perform bulk insert into storyboard_history table
        db_session.bulk_insert_mappings(StoryboardHistory, history_data)

    except:
        if pathes:
            # revert_moved_images(pathes)
            pass


def create_project_history(data):

    data.pop('created_date')
    data.pop('storyboards')
    project_id = data.pop('id', None)

    script_style = data.pop('script_style', None)
    storyboard_style = data.pop('storyboard_style', None)
    video_duration = data.pop('video_duration', None)
    aspect_ratio = data.pop('aspect_ratio', None)

    data.update({'project_id': project_id,
                 'script_style_id': script_style['id'] if script_style else None,
                 'status_id': data.pop('status')['id'],
                 'storyboard_style_id': storyboard_style['id'] if storyboard_style else None,
                 'video_duration_id': video_duration['id'] if video_duration else None,
                 'aspect_ratio_id': aspect_ratio['id'] if aspect_ratio else None,
                 })
    project_h_schema = ProjectHistorySchema()
    errors = project_h_schema.validate(data)
    if errors:
        raise Exception({'errors': errors, 'status': 400})
    project_h = ProjectHistory(
        **data
    )

    db_session.add(project_h)
    db_session.flush()
    return project_h.id


def update_project_by_id(user_id, project_id, update_data):
    history_all = ['script', 'synopsis', 'script_style_id',
                   'video_duration_id', 'storyboard_style_id', 'aspect_ratio_id']
    history_fields_script_and_storyboard = [
        'synopsis', 'script_style_id', 'video_duration_id']
    history_fields_storyboard = ['script', ]
    history_fields_storyboard_images = [
        'storyboard_style_id', 'aspect_ratio_id']
    project = Project.query.get(project_id)
    project_schema_copy = ProjectSchema()
    old_p_s = project_schema_copy.dump(project)
    project_copy_data = copy.deepcopy(old_p_s)
    create_history = False
    delete_storyboard = False
    delete_script = False
    delete_image = False
    if project and str(project.user_id) == user_id:
        for key, value in update_data.items():
            setattr(project, key, value)
            if key in history_all:
                create_history = True
                if key in history_fields_script_and_storyboard:
                    delete_script = True
                    delete_storyboard = True
                if key in history_fields_storyboard:
                    delete_storyboard = True
                if key in history_fields_storyboard_images:
                    delete_image = True
        if create_history and not (project_copy_data['script'] == None or project_copy_data['script'] == "") and \
                not (project_copy_data['synopsis'] == None or project_copy_data['synopsis'] == ""):
            project_h_id = create_project_history(project_copy_data)

            project_storyboards = db_session.query(Storyboard).filter(
                Storyboard.project_id == project_id).all()
            if project_storyboards:
                create_storyboard_history(project_h_id, project_storyboards)
                if delete_script:
                    setattr(project, 'script', "")
                    db_session.query(Storyboard).filter(
                        Storyboard.project_id == project_id).delete()
                if not delete_script:
                    if delete_storyboard:
                        db_session.query(Storyboard).filter(
                            Storyboard.project_id == project_id).delete()
                    elif delete_image:
                        for storyboard in project_storyboards:
                            storyboard.image = None

        db_session.commit()
        project_schema = ProjectSchema()
        data = project_schema.dump(project)
        return {'data': data, 'status': 200}
    return {'message': 'No data found', 'status': 404}


def delete_storyboards_by_project_id(user_id, project_id):
    try:
        project_storyboards = db_session.query(Storyboard).join(Project).\
            filter(Storyboard.project_id == project_id, Project.user_id == user_id).\
            options(joinedload(Storyboard.project)).all()
        if project_storyboards:
            for storyboard in project_storyboards:

                db_session.delete(storyboard)
            db_session.commit()
            return True
        return True
    except:
        return False


def delete_project_by_id(user_id, project_id):
    project = Project.query.get(project_id)
    if project and str(project.user_id) == user_id:

        db_session.query(Storyboard).filter(
            Storyboard.project_id == project_id).delete()
        subq = db_session.query(ProjectHistory.id).filter(
            ProjectHistory.project_id == project_id)

        db_session.query(StoryboardHistory) \
            .filter(StoryboardHistory.projects_history_id.in_(subq)) \
            .delete(synchronize_session=False)
        db_session.query(ProjectHistory).filter(
            ProjectHistory.project_id == project_id).delete()
        media_folder = os.getenv('MEDIA_FOLDER')
        project_folder = os.path.join(media_folder, str(project.id))
        try:
            shutil.rmtree(project_folder)
        except FileNotFoundError:
            pass  # Just continue execution if the folder does not exist

        db_session.delete(project)
        db_session.commit()
        data = {'message': "Project with name: "+project.name+" deleted"}
        return {'data': data, 'status': 200}
    return {'message': 'No data found', 'status': 404}


def delete_project_history_by_id(user_id, project_h_id):
    project_h = ProjectHistory.query.get(project_h_id)
    if project_h and str(project_h.project.user_id) == user_id:
        subq = db_session.query(StoryboardHistory).filter(
            StoryboardHistory.projects_history_id == project_h_id).all()
        if subq:
            images_folder = ""
            for storyboard in subq:
                if storyboard.image:
                    images_folder = storyboard.image
                    break

            db_session.query(StoryboardHistory).filter(
                StoryboardHistory.projects_history_id == project_h_id).delete()

            project_folder = os.path.dirname(images_folder)
            try:
                shutil.rmtree(project_folder)
            except FileNotFoundError:
                pass  # Just continue execution if the folder does not exist

        db_session.delete(project_h)
        db_session.commit()
        data = {'message': "Project with name: "+project_h.name+" deleted"}
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


def generate_storyboard_description(user_id, project_id, source, tries=0):
    try_count = tries+1
    try:
        project = Project.query.get(project_id)
        if project and str(project.user_id) == user_id:
            if source == 1:
                return generate_storyboards_by_synopsis(project)
            if source == 2:
                return generate_storyboards_by_script(project)
        return {'message': 'No data found', 'status': 404}
    except Exception as e:

        if try_count < 4:
            generate_storyboard_description(
                user_id, project_id, source, try_count)
        else:
            raise e


def generate_storyboards_by_synopsis(project):
    project_schema = ProjectSchema()
    synopsis = project.synopsis
    if synopsis == None or synopsis == "":
        return {'message': 'Synopsis is mandatory', 'status': 400}
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
        "source": 1
    }
    text_to_text_queue.send_message(
        message=message, routing_key=t_queue)
    try:
        project.status = Status.query.filter(
            Status.code_name == 'GeSc').first()
        db_session.commit()
    except Exception as e:
        print("error: " + str(e))
        project.status = Status.query.filter(
            Status.code_name == 'GeSc').first()
        db_session.commit()
    data = project_schema.dump(project)
    return {'data': data, 'status': 200}


def generate_storyboards_by_script(project):
    project_schema = ProjectSchema()
    script = project.script
    if script == None or script == "":
        return {'message': 'Script is mandatory', 'status': 400}
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
        "script": script,
        "script_style": script_style_name,
        "video_duration": video_duration_name,
        "source": 2
    }
    text_to_text_queue.send_message(
        message=message, routing_key=t_queue)

    try:
        project.status = Status.query.filter(
            Status.code_name == 'GeSc').first()
        db_session.commit()
    except Exception as e:
        print("error: " + str(e))
        project.status = Status.query.filter(
            Status.code_name == 'GeSc').first()
        db_session.commit()

    data = project_schema.dump(project)
    return {'data': data, 'status': 200}


def send_script(user_id, project_id, tries=0):
    try_count = tries+1
    try:
        project_schema = ProjectSchema()
        project = Project.query.get(project_id)
        if project and str(project.user_id) == user_id:

            reference = str(project.id)

            orginal_script = project.script

            prompts = {prompt.order: prompt.scene_description
                       for prompt in project.storyboards}

            aspect_ratio = project.aspect_ratio
            if aspect_ratio:
                aspect_ratio_name = aspect_ratio.name if aspect_ratio.description + \
                    f" ({aspect_ratio.description})" else ""
            else:
                return {'message': 'Aspect ratio is mandatory', 'status': 400}

            # boards_per_min = project.boards_per_min
            # if boards_per_min:
            #     boards_per_min_count = boards_per_min.count
            # else:
            #     return {'message': 'Boards per min is mandatory', 'status': 400}

            storyboard_style = project.storyboard_style
            if storyboard_style:
                storyboard_style_name = storyboard_style.description
            else:
                return {'message': 'Storyboard tyle is mandatory', 'status': 400}

            message = {
                "reference": reference,
                "orginal_script": orginal_script,
                "prompts": prompts,
                "aspect_ratio": aspect_ratio_name,
                "storyboard_style": storyboard_style_name,
                "source": 1
            }
            text_to_image_queue.send_message(
                message=message, routing_key=m_queue)
            project.status = Status.query.filter(
                Status.code_name == 'GeSt').first()
            db_session.commit()
            data = project_schema.dump(project)
            return {'data': data, 'status': 200}
        return {'message': 'No data found', 'status': 404}
    except Exception as e:
        if try_count < 4:
            send_script(user_id, project_id, try_count)
        else:
            raise e


def update_regenerate_storyboard(user_id, storyboard_id, scene_description, tries=0):
    try_count = tries+1
    try:
        project_schema = ProjectSchema()
        storyboard_query = Storyboard.query.get(storyboard_id)
        storyboard = storyboard_query
        project = storyboard.project
        old_p_data = project_schema.dump(project)
        if project and str(project.user_id) == user_id:

            # insert project and storyboards in history
            project_h_id = create_project_history(old_p_data)
            project_storyboards = db_session.query(Storyboard).filter(
                Storyboard.project_id == project.id).all()
            create_storyboard_history(project_h_id, project_storyboards)
            db_session.flush()

            reference = str(storyboard.id)

            orginal_script = project.script
            storyboard.scene_description = scene_description
            storyboard.image = None
            prompts = {storyboard.order: scene_description}

            aspect_ratio = project.aspect_ratio
            if aspect_ratio:
                aspect_ratio_name = aspect_ratio.name if aspect_ratio.description + \
                    f" ({aspect_ratio.description})" else ""
            else:
                return {'message': 'Aspect ratio is mandatory', 'status': 400}

            storyboard_style = project.storyboard_style
            if storyboard_style:
                storyboard_style_name = storyboard_style.name + \
                    f" ({storyboard_style.description}) "
            else:
                return {'message': 'Storyboard tyle is mandatory', 'status': 400}

            message = {
                "reference": reference,
                "orginal_script": orginal_script,
                "prompts": prompts,
                "aspect_ratio": aspect_ratio_name,
                "storyboard_style": storyboard_style_name,
                "source": 2
            }
            text_to_image_queue.send_message(
                message=message, routing_key=m_queue)
            project.status = Status.query.filter(
                Status.code_name == 'GeSt').first()
            db_session.commit()
            data = project_schema.dump(project)
            return {'data': data, 'status': 200}
        return {'message': 'No data found', 'status': 404}
    except Exception as e:
        if try_count < 4:
            update_regenerate_storyboard(
                user_id, storyboard_id, scene_description, try_count)
        else:
            raise e


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


def on_emit_acknowledgment(response):
    print("Server acknowledgment:", response)


def set_scribt_storyboard_desc(data, db_session, for_consumer=True, socket=None):
    dict_data = json.loads(data)
    source = dict_data['source']
    if source == 1:
        set_scribt_and_storyboard_desc(dict_data, db_session, for_consumer)
    if source == 2:
        set_storyboard_desc(dict_data, db_session, for_consumer=True)
    ref = dict_data['reference']
    socket.emit('project_status_updated', {
        'project_id': ref,
        'message': 'Project status updated'
    })


def set_scribt_and_storyboard_desc(dict_data, db_session, for_consumer=True):
    try:

        storyboards_list = []
        project_id = dict_data['reference']
        project = Project.query.get(project_id)
        success = dict_data['success']
        project_script = dict_data.get('script', None)
        if project:
            if success == 1:
                db_session.query(Storyboard).filter(
                    Storyboard.project_id == project.id).delete()
                storyboards = dict_data['storyboards']

                project.script = project_script
                for key, value in storyboards.items():
                    storyboard_data = {
                        'project_id': project.id,
                        'order': key,
                        'scene_description': str(value),
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

                error = dict_data['e_message']
                raise Exception(error)
        return "error"
    except Exception as e:
        project.status = Status.query.filter(
            Status.code_name == 'Wa').first()
        db_session.commit()
        if for_consumer:
            # insert in error table
            t2t_error_processing(project_id, str(e),
                                 project_script, db_session)
            return
        else:
            raise e


def set_storyboard_desc(dict_data, db_session, for_consumer=True):
    try:

        storyboards_list = []
        project_id = dict_data['reference']
        project = Project.query.get(project_id)
        success = dict_data['success']
        # project_script = dict_data.get('script', None)
        if project:
            if success == 1:
                db_session.query(Storyboard).filter(
                    Storyboard.project_id == project.id).delete()
                storyboards = dict_data['storyboards']

                # project.script = project_script
                for key, value in storyboards.items():
                    storyboard_data = {
                        'project_id': project.id,
                        'order': key,
                        'scene_description': str(value),
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

                error = dict_data['e_message']
                raise Exception(error)
        return "error"
    except Exception as e:
        project.status = Status.query.filter(
            Status.code_name == 'Wa').first()
        db_session.commit()
        if for_consumer:
            # insert in error table
            t2t_error_processing(project_id, str(e),
                                 str(storyboards), db_session)
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


def set_storyboard_image(data, db_session, for_consumer=True, socket=None):
    dict_data = json.loads(data)
    source = dict_data["source"]
    if source == 1:
        return set_scribt_storyboard_images(dict_data, db_session, for_consumer, socket)
    if source == 2:
        return update_storyboard_image(dict_data, db_session, for_consumer, socket)


def set_scribt_storyboard_images(dict_data, db_session, for_consumer=True, socket=None):
    try:
        project_id = dict_data['reference']
        project = Project.query.get(project_id)
        success = dict_data['success']
        images_data = dict_data.get('images_data', None)
        if project:
            if success == 1:

                storyboards = db_session.query(Storyboard).filter_by(
                    project_id=project.id).order_by(Storyboard.order).all()
                for storyboard in storyboards:
                    storyboard.image = images_data[str(storyboard.order)]

                project.status = Status.query.filter(
                    Status.code_name == 'GedSt').first()
                db_session.commit()

                socket.emit('project_status_updated', {
                    'project_id': project_id,
                    'message': 'Project status updated'
                })
                return
            else:

                error = dict_data['e_message']
                raise Exception(error)
        return "error"
    except Exception as e:
        project.status = Status.query.filter(
            Status.code_name == 'GedSc').first()
        db_session.commit()
        if for_consumer:
            # insert in error table
            t2i_error_processing(project_id, str(e),
                                 str(images_data), db_session)
            return
        else:
            raise e


def update_storyboard_image(dict_data, db_session, for_consumer=True, socket=None):
    try:
        storyboard_id = dict_data['reference']
        storyboard = Storyboard.query.get(storyboard_id)
        project = storyboard.project
        project_id = project.id
        success = dict_data['success']
        images_data = dict_data.get('images_data', None)
        if project:
            if success == 1:
                storyboard.image = images_data[str(storyboard.order)]

                project.status = Status.query.filter(
                    Status.code_name == 'GedSt').first()
                db_session.commit()

                socket.emit('project_status_updated', {
                    'project_id': project_id,
                    'message': 'Project status updated'
                })
                return
            else:

                error = dict_data['e_message']
                raise Exception(error)
        return "error"
    except Exception as e:
        project.status = Status.query.filter(
            Status.code_name == 'GedSc').first()
        db_session.commit()
        if for_consumer:
            # insert in error table
            t2i_error_processing(project_id, str(e),
                                 str(images_data), db_session)
            return
        else:
            raise e


def t2t_consumer_bl(db_session, socket):
    try:
        callback_func = text_to_text_n_queue.create_callback(
            set_scribt_storyboard_desc, db_session, socket)
        text_to_text_n_queue.consumer(queue=os.getenv(
            'RMQ_T2T_N_QUEUE'), callback=callback_func)
    except Exception as e:
        print(f"An error occurred: {e}")
        db_session.rollback()
    finally:
        db_session.close()


def t2m_consumer_bl(db_session, socket):
    try:
        callback_func = text_to_image_n_queue.create_callback(
            set_storyboard_image, db_session, socket)
        text_to_image_n_queue.consumer(queue=os.getenv(
            'RMQ_T2M_N_QUEUE'), callback=callback_func)
    except Exception as e:
        print(f"An error occurred: {e}")
        db_session.rollback()
    finally:
        db_session.close()

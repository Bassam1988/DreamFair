from marshmallow import Schema, fields
from dotenv import load_dotenv
import os

from .schemas import AspectRatioSchema, BoardsPerMinSchema, ProjectSchema, ScriptStyleSchema, StatusSchema, StoryBoardStyleSchema, VideoDurationSchema

load_dotenv()


class StoryboardHistoryProjectHistorySchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    image = fields.Method("format_image_url")
    scene_description = fields.Str()
    project_history_id = fields.UUID(load_only=True)

    def format_image_url(self, obj):
        base_url = os.getenv('MEDIA_BASE_URL')
        if hasattr(obj, 'image'):
            if obj.image and base_url:
                return f"{base_url}{obj.image.replace('/home/ubuntu/media/', '')}"
            return obj.image
        return None


class ProjectHistoryListSchema(Schema):
    id = fields.UUID(dump_only=True)
    created_date = fields.Date(dump_only=True)

    script_style_id = fields.UUID(load_only=True)
    script_style = fields.Nested(ScriptStyleSchema, dump_only=True)

    status_id = fields.UUID(load_only=True)
    status = fields.Nested(StatusSchema, dump_only=True)

    storyboard_style_id = fields.UUID(load_only=True)
    storyboard_style = fields.Nested(StoryBoardStyleSchema, dump_only=True)

    video_duration_id = fields.UUID(load_only=True)
    video_duration = fields.Nested(VideoDurationSchema, dump_only=True)

    aspect_ratio_id = fields.UUID(load_only=True)
    aspect_ratio = fields.Nested(AspectRatioSchema, dump_only=True)

    boards_per_min_id = fields.UUID(load_only=True)
    boards_per_min = fields.Nested(BoardsPerMinSchema, dump_only=True)

    storyboards_history = fields.Nested(
        StoryboardHistoryProjectHistorySchema, many=True, dump_only=True)  # type: ignore


class ProjectHistorySchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    synopsis = fields.Str(required=False)
    script = fields.Str(required=False)
    created_date = fields.Date(dump_only=True)

    project_id = fields.UUID(load_only=True)
    project = fields.Nested(ProjectSchema, dump_only=True)

    script_style_id = fields.UUID(load_only=True)
    script_style = fields.Nested(ScriptStyleSchema, dump_only=True)

    status_id = fields.UUID(load_only=True)
    status = fields.Nested(StatusSchema, dump_only=True)

    storyboard_style_id = fields.UUID(load_only=True)
    storyboard_style = fields.Nested(StoryBoardStyleSchema, dump_only=True)

    video_duration_id = fields.UUID(load_only=True)
    video_duration = fields.Nested(VideoDurationSchema, dump_only=True)

    aspect_ratio_id = fields.UUID(load_only=True)
    aspect_ratio = fields.Nested(AspectRatioSchema, dump_only=True)

    boards_per_min_id = fields.UUID(load_only=True)
    boards_per_min = fields.Nested(BoardsPerMinSchema, dump_only=True)

    storyboards_history = fields.Nested(
        StoryboardHistoryProjectHistorySchema, many=True, dump_only=True)  # type: ignore


class StoryboardSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    image = fields.Str()
    order = fields.Int()
    scene_description = fields.Str()
    project_history_id = fields.UUID(load_only=True)
    project_history = fields.Nested(
        StoryboardHistoryProjectHistorySchema, dump_only=True)


class StoryboardHistoryCreateSchema(Schema):
    name = fields.Str(required=True)
    image = fields.Str()
    order = fields.Int()
    scene_description = fields.Str()

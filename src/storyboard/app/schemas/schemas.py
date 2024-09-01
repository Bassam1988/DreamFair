# schemas.py
from marshmallow import Schema, fields
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class ScriptStyleSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str()
    code_name = fields.Str()


class StoryBoardStyleSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str()
    code_name = fields.Str()


class VideoDurationSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str()
    code_name = fields.Str()


class AspectRatioSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str()
    code_name = fields.Str()


class BoardsPerMinSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str()
    count = fields.Integer()
    code_name = fields.Str()


class StoryboardProjectSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    image = fields.Method("format_image_url")
    scene_description = fields.Str()
    project_id = fields.UUID(load_only=True)

    def format_image_url(self, obj):
        base_url = os.getenv('MEDIA_BASE_URL')
        if obj.image and base_url:
            return f"{base_url}{obj.image.replace('/home/ubuntu/media/', '')}"
        return obj.image


class StatusSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str()
    code_name = fields.Str()


class ProjectSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    synopsis = fields.Str(required=False)
    script = fields.Str(required=False)
    script_style_id = fields.UUID(load_only=True)
    script_style = fields.Nested(ScriptStyleSchema, dump_only=True)
    status = fields.Nested(StatusSchema, dump_only=True)

    storyboard_style_id = fields.UUID(load_only=True)
    storyboard_style = fields.Nested(StoryBoardStyleSchema, dump_only=True)

    video_duration_id = fields.UUID(load_only=True)
    video_duration = fields.Nested(VideoDurationSchema, dump_only=True)

    aspect_ratio_id = fields.UUID(load_only=True)
    aspect_ratio = fields.Nested(AspectRatioSchema, dump_only=True)

    boards_per_min_id = fields.UUID(load_only=True)
    boards_per_min = fields.Nested(BoardsPerMinSchema, dump_only=True)

    storyboards = fields.Nested(
        StoryboardProjectSchema, many=True, dump_only=True)  # type: ignore


# class StoryboardProjectSchema(Schema):
#     id = fields.UUID(dump_only=True)
#     name = fields.Str(required=True)


class StoryboardSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    image = fields.Str()
    order = fields.Int()
    scene_description = fields.Str()
    project_id = fields.UUID(load_only=True)
    project = fields.Nested(StoryboardProjectSchema, dump_only=True)


class T2TOperationErrorSchema(Schema):
    id = fields.UUID(dump_only=True)
    reference = fields.Str(required=True)
    script_text = fields.Str(required=True)
    error = fields.Str(required=True)
    created_date = fields.Date(dump_only=True)


class T2IOperationErrorSchema(Schema):
    id = fields.UUID(dump_only=True)
    reference = fields.Str(required=True)
    script_text = fields.Str(required=True)
    error = fields.Str(required=True)
    created_date = fields.Date(dump_only=True)

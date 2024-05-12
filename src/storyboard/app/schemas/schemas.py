# schemas.py
from marshmallow import Schema, fields


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
    image = fields.Str()
    scene_description = fields.Str()
    project_id = fields.UUID(load_only=True)


class ProjectSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    synopsis = fields.Str()
    script = fields.Str()
    script_style_id = fields.UUID(load_only=True)
    script_style = fields.Nested(ScriptStyleSchema, dump_only=True)

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


class StoryboardProjectSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)


class StoryboardSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    image = fields.Str()
    scene_description = fields.Str()
    project_id = fields.UUID(load_only=True)
    project = fields.Nested(StoryboardProjectSchema, dump_only=True)

# schemas.py
from marshmallow import Schema, fields


class StoryboardText2TextOperationSchema(Schema):
    id = fields.UUID(dump_only=True)
    generated_text = fields.Str(dump_only=True)
    order = fields.Int(dump_only=True)


class Text2TextOperationSchema(Schema):
    id = fields.UUID(dump_only=True)
    reference = fields.Str(required=True)
    original_text = fields.Str()
    generated_text = fields.Str()
    generated_script = fields.Str()
    storyboards = fields.Nested(
        StoryboardText2TextOperationSchema, many=True, dump_only=True)  # type: ignore


class Text2TextOperationStoryboardSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)


class StoryboardSchema(Schema):
    id = fields.UUID(dump_only=True)
    generated_text = fields.Str(required=True)
    order = fields.Int()
    scene_description = fields.Str()
    text2text_operation_id = fields.UUID(load_only=True)
    text2text_operation = fields.Nested(
        Text2TextOperationStoryboardSchema, dump_only=True)

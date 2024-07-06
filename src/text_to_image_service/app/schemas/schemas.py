# schemas.py
from marshmallow import Schema, fields


class ImageText2ImageOperationSchema(Schema):
    id = fields.UUID(dump_only=True)
    scene_text = fields.Str(dump_only=True)
    order = fields.Int(dump_only=True)
    url = fields.Str(dump_only=True)


class Text2ImageOperationSchema(Schema):
    id = fields.UUID(dump_only=True)
    reference = fields.Str(required=True)
    script_text = fields.Str()
    images = fields.Nested(
        ImageText2ImageOperationSchema, many=True, dump_only=True)  # type: ignore


class Text2ImageOperationImagesSchema(Schema):
    id = fields.UUID(dump_only=True)
    reference = fields.Str(dump_only=True)


class ImagesSchema(Schema):
    id = fields.UUID(dump_only=True)
    scene_text = fields.Str(required=True)
    order = fields.Int(required=True)
    url = fields.Str(required=True)
    text2image_operation_id = fields.UUID(load_only=True)
    text2image_operation = fields.Nested(
        Text2ImageOperationImagesSchema, dump_only=True)


class OperationErrorSchema(Schema):
    id = fields.UUID(dump_only=True)
    reference = fields.Str(required=True)
    script_text = fields.Str(required=True)
    error = fields.Str(required=True)
    created_date = fields.Date(dump_only=True)

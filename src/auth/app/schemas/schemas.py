# schemas.py
from marshmallow import Schema, fields


class RoleSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str()


class UserSchema(Schema):
    id = fields.UUID(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True)
    roles = fields.Nested(RoleSchema, many=True, dump_only=True)
    role_ids = fields.List(fields.UUID(), load_only=True)

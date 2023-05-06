from marshmallow import Schema, fields


class UserHypermediaSchema(Schema):
    self = fields.Url()
    followers = fields.Url()
    followed = fields.Url()
    avatar = fields.Url()

# Might not need
class PlainUserSchema(Schema):
    user_id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    last_seen = fields.DateTime()
    about_me = fields.Str()

class UserDataSchema(PlainUserSchema):
    user_id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=False)
    last_seen = fields.DateTime()
    about_me = fields.Str()
    post_count = fields.Int()
    follower_count = fields.Int()
    followed_count = fields.Int()
    _links = fields.Nested(UserHypermediaSchema(), dump_only=True)

# TODO: Need to expand
class UserUpdateSchema(Schema):
    username = fields.Str()
    email = fields.Str()

# TODO:  Need to expand
class UserRegisterSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Str(required=True)
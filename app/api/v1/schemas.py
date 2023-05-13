from marshmallow import Schema, fields


class UserHypermediaSchema(Schema):
    self = fields.Url()
    followers = fields.Url()
    followed = fields.Url()
    avatar = fields.Url()


class UsersCollectionMetaSchema(Schema):
    page = fields.Int()
    per_page = fields.Int()
    total_pages = fields.Int()
    total_items = fields.Int()


class UsersCollectionLinkSchema(Schema):
    self = fields.Url()
    next = fields.Url()
    prev = fields.Url()


# Might not need
class PlainUserSchema(Schema):
    user_id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=False)
    last_seen = fields.DateTime()
    about_me = fields.Str()


class UserDataSchema(PlainUserSchema):
    user_id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=False)
    last_seen = fields.DateTime()
    about_me = fields.Str()
    post_count = fields.Int()
    follower_count = fields.Int()
    followed_count = fields.Int()
    _links = fields.Nested(UserHypermediaSchema(), dump_only=True)


class UsersCollectionDataSchema(Schema):
    items = fields.List(fields.Nested(UserDataSchema()))
    _meta = fields.Nested(UsersCollectionMetaSchema(), dump_only=True)
    _links = fields.Nested(UsersCollectionLinkSchema(), dump_only=True)


class UserRegisterSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class UserUpdateSchema(Schema):
    username = fields.Str()
    email = fields.Email()
    about_me = fields.Str()

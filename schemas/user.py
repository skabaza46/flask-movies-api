from marsh.ma import ma
from models.user import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        models = User
        load_instance = True
        fields = ("movie_id", "name")


user_schema = UserSchema()
user_schema = UserSchema(many=True)

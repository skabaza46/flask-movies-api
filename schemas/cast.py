from marsh.ma import ma

from models.cast import Cast


class CastSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cast
        load_instance = True
        fields = ("movie_id", "name")


cast_schema = CastSchema()
casts_schema = CastSchema(many=True)

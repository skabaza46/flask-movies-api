from marsh.ma import ma
from models.director import Director


class DirectorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        models = Director
        load_instance = True
        fields = ("movie_id", "name")


director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

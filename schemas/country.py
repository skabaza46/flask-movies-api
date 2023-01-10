from marsh.ma import ma
from models.country import Country


class CountrySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        models = Country
        load_instance = True
        fields = ("movie_id", "name")


country_schema = CountrySchema()
countrys_schema = CountrySchema(many=True)

from marshmallow import fields

# from utils.pagination import PaginationSchema
from .cast import CastSchema
from .listing import ListingSchema
from .director import DirectorSchema
from .country import CountrySchema
from marsh.ma import ma
from models.movie import Movie


class MovieSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movie
        load_instance = True
        fields = (
            "title",
            "type",
            "date_added",
            "release_year",
            "rating",
            "duration",
            "description",
            "directors",
            "casts",
            "listings",
            "countrys",
        )

    directors = fields.Nested(DirectorSchema, many=True)
    casts = fields.Nested(CastSchema, many=True)
    listings = fields.Nested(ListingSchema, many=True)
    countrys = fields.Nested(CountrySchema, many=True)


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

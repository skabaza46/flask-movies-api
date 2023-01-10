from marsh.ma import ma
from models.listing import Listing


class ListingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        models = Listing
        load_instance = True
        fields = ("movie_id", "name")


listing_schema = ListingSchema()
listings_schema = ListingSchema(many=True)

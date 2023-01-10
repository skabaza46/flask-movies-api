from sqlalchemy.orm import relationship
from alchemy_db.db import db
from .cast import Cast
from .country import Country
from .director import Director
from .listing import Listing


class Movie(db.Model):
    id = db.Column("show_id", db.Integer, primary_key=True)
    type = db.Column(db.String(250))
    title = db.Column(db.String(250))
    date_added = db.Column(db.String(250))
    release_year = db.Column(db.String(250))
    rating = db.Column(db.String(250))
    duration = db.Column(db.String(250))
    description = db.Column(db.String(250))
    countrys = relationship("Country", backref="movie", uselist=True)
    directors = relationship("Director", backref="movie", uselist=True)
    casts = relationship("Cast", backref="movie", uselist=True)
    listings = relationship("Listing", backref="movie", uselist=True)

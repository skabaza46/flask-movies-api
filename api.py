from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import or_
from flask_marshmallow import Marshmallow
from marshmallow import fields
from utils.pagination import PaginationSchema

from flask_restful import Api
from flask_rest_paginate import Pagination
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config[
    "SECRET_KEY"
] = "310999c0-4690-455c-9e5c-061957778915"  # fake key for development***
app.config["CORS_HEADERS"] = "Content-Type"


db = SQLAlchemy(app)

pagination = Pagination(app, db)

ma = Marshmallow(app)

cors = CORS(app)


class Cast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.show_id"))
    name = db.Column(db.String(250))

    def __repr__(self):
        return f'<Cast "{self.name}">'


class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.show_id"))
    name = db.Column(db.String(250))

    def __repr__(self):
        return f'<Director "{self.name}">'


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.show_id"))
    name = db.Column(db.String(250))

    def __repr__(self):
        return f'<Listing "{self.name}">'


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.show_id"))
    name = db.Column(db.String(250))

    def __repr__(self):
        return f'<Country "{self.name}">'


class Movie(db.Model):
    id = db.Column("show_id", db.Integer, primary_key=True)
    type = db.Column(db.String(250))
    title = db.Column(db.String(250))
    countrys = db.relationship("Country", backref="movie", uselist=True)
    date_added = db.Column(db.String(250))
    release_year = db.Column(db.String(250))
    rating = db.Column(db.String(250))
    duration = db.Column(db.String(250))
    description = db.Column(db.String(250))
    directors = db.relationship("Director", backref="movie", uselist=True)
    casts = db.relationship("Cast", backref="movie", uselist=True)
    listings = db.relationship("Listing", backref="movie", uselist=True)


class CastSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cast
        # Fields to expose
        fields = ("movie_id", "name")


class ListingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        models = Listing
        # Fields to expose
        fields = ("movie_id", "name")


class DirectorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        models = Director
        # Fields to expose
        fields = ("movie_id", "name")


class CountrySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        models = Country
        # Fields to expose
        fields = ("movie_id", "name")


class MovieSchema(ma.SQLAlchemyAutoSchema, PaginationSchema):
    directors = fields.Nested(DirectorSchema, many=True)
    casts = fields.Nested(CastSchema, many=True)
    listings = fields.Nested(ListingSchema, many=True)
    countrys = fields.Nested(CountrySchema, many=True)

    class Meta:
        model = Movie
        # Fields to expose
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


cast_schema = CastSchema()
casts_schema = CastSchema(many=True)

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

listing_schema = ListingSchema()
listings_schema = ListingSchema(many=True)

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

country_schema = CountrySchema()
countrys_schema = CountrySchema(many=True)


@app.route("/movies/<int:id>", methods=["GET"])
@app.route("/movies", methods=["GET"])
@cross_origin()
def get_movies(id=None):

    if not id:
        # movies = Movie.query.all()

        response = pagination.paginate(Movie, movies_schema, True)

        return response
    else:
        movie = Movie.query.get(id)

        serialized_data = movie_schema.dump(movie)
        if movie:
            return jsonify(movie=serialized_data, status=200)
        else:
            return jsonify(movie=serialized_data, status=404)


@app.route("/search/<searchVar>", methods=["GET"])
@app.route("/search", methods=["GET"])
@cross_origin()
def search(searchVar=None):
    if not searchVar:
        response = pagination.paginate(Movie, movies_schema, True)
        return response

    else:

        query = Movie.query.filter(
            or_(
                Movie.title.contains(searchVar),
                Movie.type.contains(searchVar),
                Movie.date_added.contains(searchVar),
                Movie.release_year.contains(searchVar),
                Movie.rating.contains(searchVar),
                Movie.rating.contains(searchVar),
                Movie.duration.contains(searchVar),
                Movie.description.contains(searchVar),
            )
        )

        response = pagination.paginate(query, movies_schema, True)
        return response


if __name__ == "__main__":

    app.run(debug=True)

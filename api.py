import argparse
from flask import Flask, jsonify
from sqlalchemy import or_
from flask_rest_paginate import Pagination
from flask_cors import CORS, cross_origin

from models.movie import Movie
from schemas.movie import movie_schema, movies_schema
from marsh.ma import ma
from alchemy_db.db import db
from settings import settings
from migrations import initialize_db as initialize_db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
app.config["SECRET_KEY"] = settings.SECRET_KEY
app.config["API_KEY"] = settings.API_KEY

pagination = Pagination(app, db)

cors = CORS(app)


@app.route("/movies/<int:id>", methods=["GET"])
@app.route("/movies", methods=["GET"])
@cross_origin()
def get_movies(id=None):

    if not id:
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

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--migrate",
        help="Migrate the data from the csv file to the database",
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "--run", help="Start the api service", action=argparse.BooleanOptionalAction
    )
    args = parser.parse_args()

    if args.migrate != None:
        db.init_app(app)

        stars = "*" * 5

        print("{} Migrating Data to Database {}".format(stars, stars))

        with app.app_context():

            db.drop_all()
            db.create_all()
            initialize_db.run_data_migration()

    if args.run != None:
        db.init_app(app)
        ma.init_app(app)
        app.run(debug=True)

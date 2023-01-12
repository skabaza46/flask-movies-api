import argparse
import uuid
import os
import datetime
from flask import Flask, jsonify, request, session
from flask_bcrypt import Bcrypt

from sqlalchemy import or_
from sqlalchemy.orm import load_only
from sqlalchemy import func

from flask_rest_paginate import Pagination
from flask_cors import CORS, cross_origin

from models.movie import Movie
from models.cast import Cast
from models.director import Director
from models.country import Country
from models.listing import Listing
from models.user import User

from schemas.movie import movie_schema, movies_schema
from marsh.ma import ma
from alchemy_db.db import db
from settings import settings
from migrations import initialize_db as initialize_db
from utils.clean_movie_field_strings import clean as clean_field

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
app.config["SECRET_KEY"] = settings.SECRET_KEY
app.config["API_KEY"] = settings.API_KEY

pagination = Pagination(app, db)

cors = CORS(app)
bcrypt = Bcrypt(app)


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


@app.route("/statistics/<int:release_year>", methods=["GET"])
@app.route("/statistics", methods=["GET"])
@cross_origin()
def statistics(release_year=None):
    """Create statistics data for the dashboard."""
    if not release_year:
        latest_movie = Movie.query.order_by(Movie.release_year.desc()).first()
        if latest_movie.release_year:
            release_year = latest_movie.release_year
        else:
            release_year = datetime.date.today().year

    movies = Movie.query.filter(Movie.release_year == release_year)

    # Create the structure of the payload
    data_points = {
        "movies_year": release_year,
        "total_movies": movies.count(),
        "total_directors": 0,
        "ratings": {},
        "types": {},
        "listings": {},
    }

    for movie in movies:
        rating = (movie.rating.lower()).replace("-", "_")
        movie_type = (movie.type.lower()).replace(" ", "_")
        listings = [
            {clean_field(i.name): 0, "name": i.name, "key": clean_field(i.name)}
            for i in movie.listings
        ]

        if rating not in data_points["ratings"].keys():
            data_points["ratings"].update({rating: {"total": 1, "name": movie.rating}})
        else:
            data_points["ratings"][rating]["total"] += 1

        if movie_type not in data_points["types"].keys():
            data_points["types"].update(
                {movie_type: {"total": 1, "name": movie.rating}}
            )
        else:
            data_points["types"][movie_type]["total"] += 1

        for item in listings:
            listing_name = item.get("name")
            listing_key = item.get("key")

            if listing_key not in data_points["listings"].keys():
                data_points["listings"].update(
                    {listing_key: {"total": 1, "name": listing_name}}
                )
            else:
                data_points["listings"][listing_key]["total"] += 1

    new_listings = [data_points["listings"][i] for i in data_points["listings"]]
    data_points["listings"] = new_listings

    types = [data_points["types"][i] for i in data_points["types"].keys()]
    data_points["types"] = types

    ratings = [data_points["ratings"][i] for i in data_points["ratings"].keys()]
    data_points["ratings"] = ratings

    return jsonify(data=data_points)


@app.route("/user/register", methods=["POST"])
@cross_origin()
def user_register():
    json_data = request.json

    missing_fields = []
    email = json_data.get("email")
    password = json_data.get("password")
    last_name = json_data.get("last_name")
    first_name = json_data.get("first_name")

    if not email:
        missing_fields.append("email")

    if not password:
        missing_fields.append("password")
    first_name = json_data.get("first_name")
    if not first_name:
        missing_fields.append("first_name")

    if not last_name:
        missing_fields.append("last_name")

    if len(missing_fields) > 0:
        fields_required = ", ".join(missing_fields)
        message = "Missing required fields: {}".format(fields_required)
        return jsonify(data=message), 400

    # Check to see if the user already exists in the system
    exists = User.query.filter(User.email == email).first() is not None

    if exists:
        status = "User already exists in the system!"
        return jsonify(data=status), 400

    hashed_password = bcrypt.generate_password_hash(password)

    user = User(
        email=email,
        password=hashed_password,
        first_name=first_name,
        last_name=last_name,
    )

    try:
        db.session.add(user)
        db.session.commit()
        # token = user.encode_token(user)

        responseObject = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }

        return jsonify(data=responseObject), 201
    except Exception as error:
        # raise error
        status = "Something went wrong during, user creation!"
        db.session.close()
        return jsonify(data=status), 400


@app.route("/user/login", methods=["POST"])
@cross_origin()
def login():
    json_data = request.json

    missing_fields = []
    email = json_data.get("email")
    password = json_data.get("password")

    if not email:
        missing_fields.append("email")

    if not password:
        missing_fields.append("password")

    if len(missing_fields) > 0:
        fields_required = ", ".join(missing_fields)
        message = "Missing required fields: {}".format(fields_required)
        return jsonify(data=message), 400

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, json_data["password"]):

        session["logged_in"] = True
        token = user.encode_token(user)
        if token:
            responseObject = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "token": token,
            }

        return jsonify(data=responseObject), 200
    else:
        status = "Failed to log in!"
        return jsonify(data=status), 401


@app.route("/user/logout")
@cross_origin()
def logout():
    session.pop("logged_in", None)
    return jsonify(dara="Logged out!"), 200


if __name__ == "__main__":
    stars = "*" * 5

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--migrate",
        help="Migrate the data from the csv file to the database",
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "--recreate_tables",
        help="Recreates tables in the database.",
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "--run", help="Start the api service", action=argparse.BooleanOptionalAction
    )
    args = parser.parse_args()

    if args.recreate_tables != None:
        db.init_app(app)

        print("{} Recreating tables in the database {}".format(stars, stars))

        with app.app_context():
            db.drop_all()
            db.create_all()

    if args.migrate != None:
        db.init_app(app)

        print("{} Migrating Data to Database {}".format(stars, stars))

        with app.app_context():

            db.drop_all()
            db.create_all()
            initialize_db.run_data_migration()

    if args.run != None:
        db.init_app(app)
        ma.init_app(app)
        app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
        # app.run(debug=True, threaded=True)


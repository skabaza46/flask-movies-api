from api import db, Cast, Director, Country, Listing, Movie, app
from utils.clean_csv_data import cleansed_csv_data

def data_constructor(datas, model_type):
    model_type = model_type.lower()

    new_data = []
    for data in datas:
        if model_type == "cast":
            new_data.append(Cast(name=data))

        if model_type == "director":
            new_data.append(Director(name=data))

        if model_type == "listing":
            new_data.append(Listing(name=data))

        if model_type == "country":
            new_data.append(Country(name=data))

    return new_data


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()

        movies = cleansed_csv_data()
        for movie in movies:

            casts = data_constructor(datas=movie.get("cast", []), model_type="Cast")

            directors = data_constructor(datas=movie.get("director", []), model_type="Director")

            listings = data_constructor(datas=movie.get("listed_in", []), model_type="Listing")

            countrys = data_constructor(datas=movie.get("country", []), model_type="Country")

            created_movie = Movie(
                title=movie.get("title", ""),
                date_added=movie.get("date_added", ""),
                release_year=movie.get("release_year", ""),
                type=movie.get("type", ""),
                rating=movie.get("rating", ""),
                duration=movie.get("duration", ""),
                description=movie.get("description", ""),
                casts=casts,
                directors=directors,
                listings=listings,
                countrys=countrys,
               )

            print("\nCasts: {}".format(casts))
            print("\nDirectors: {}".format(directors))
            print("\nListings: {}".format(listings))
            print("\nCountrys: {}".format(countrys))

            print(countrys)


            db.session.add_all([*casts,*directors, *listings, *countrys])
            db.session.add_all([created_movie])

            db.session.commit()







# import pandas
"""Cleans and transforms the data coming from the csv file."""
import csv


def string_to_list(text, delimeter=","):
    """Transforms strings into a list, given a delimeter."""
    new_text = text.split(delimeter)
    return new_text


def cleansed_csv_data(file_path="data/netflix_titles.csv", show_output=False):
    """Cleans and transformas the csv file data, and returns the list of new data."""
    movies_list = []
    with open(file_path) as csvfile:
        csv_reader = csv.DictReader(csvfile)

        for row in csv_reader:
            director = row.get("director", "")
            if director:
                row["director"] = string_to_list(director)
            else:
                row["director"] = []

            cast = row.get("cast", "")
            if cast:
                row["cast"] = string_to_list(cast)
            else:
                row["cast"] = []

            country = row.get("country", "")
            if country:
                row["country"] = string_to_list(country)
            else:
                row["country"] = []

            listed_in = row.get("listed_in", "")
            if listed_in:
                row["listed_in"] = string_to_list(listed_in)
            else:
                row["listed_in"] = []

            if show_output:
                print("\nMovie: {}".format(row))

            movies_list.append(row)

    return movies_list


if __name__ == "__main__":
    cleansed_csv_data()

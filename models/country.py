from alchemy_db.db import db


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.show_id"))
    name = db.Column(db.String(250))

    def __repr__(self):
        return f'<Country "{self.name}">'

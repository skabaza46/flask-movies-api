import datetime
import jwt


from alchemy_db.db import db
from settings import settings


class User(db.Model):
    __table_args__ = (
        # this can be db.PrimaryKeyConstraint if you want it to be a primary key
        db.UniqueConstraint("email", "first_name", "last_name"),
    )
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250))
    first_name = db.Column(db.String(250))
    last_name = db.Column(db.String(250))
    password = db.Column(db.String(250))

    def __repr__(self):
        return f'<User "{self.email}">'

    def encode_token(self, user):
        """Generates the Auth Token:return: string"""
        try:

            payload = {
                "expire": str(
                    datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5)
                ),
                "issued_at": str(datetime.datetime.utcnow()),
                "sub": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "id": user.id,
                },
            }

            return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        except Exception as e:
            return e

    def decode_token(self, token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")

            return {
                "user": payload["sub"],
                "message": "Signature expired. Please log in again.",
            }

        except jwt.ExpiredSignatureError:

            return {"user": None, "message": "Signature expired. Please log in again."}
        except jwt.InvalidSignatureError:
            return {"user": None, "message": "Signature verification failed."}
        except Exception as error:

            return {
                "user": None,
                "message": "Something went wrong while trying to validate token.",
            }

# flask-movies-api
A Flask API Serving movie data

## Setup Instructions
### Create a .env file in the root directory, with the below variables
```
SQLALCHEMY_DATABASE_URI=""
SQLALCHEMY_TRACK_MODIFICATIONS=True|False
SECRET_KEY=""
```

### Install Pipenv
```
pipenv install
```
### Start virtual environment
```
pipenv shell
```
### Install project dependencies
```
pipenv install -r requirements.txt
```

### Migrate data into the database
#### Run below command while in project working directory
```
python app.py --migrate
```
### Start the API
#### Runt below command, starts at port=5000 by default
```
python app.py --run
```

## Endpoints
### GET all movies, returns paginated response
```
http://127.0.0.1:5000/movies
```

### GET a particular movie, returns json
```
http://127.0.0.1:5000/movies/<int:id>
```
### GET Search all movies based on the provided value, returns paginated response
```
http://127.0.0.1:5000/search/91 min
```

# flask-movies-api
A Flask API Serving movie data

## Setup Instructions
### Create a .env file in the root directory, with the below variables
```
SQLALCHEMY_DATABASE_URI="sqlite:///movies.db"
SQLALCHEMY_TRACK_MODIFICATIONS=False
SECRET_KEY="60e04612-edfa-4ad0-b9f4-8cab1616397d"
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
python api.py --migrate
```
### Start the API
#### Runt below command, starts at port=5000 by default
```
python api.py --run
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

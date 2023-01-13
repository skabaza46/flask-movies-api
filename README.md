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
python api.py --migrate
```
### Start the API without Docker or Docker Compose
#### Start the service at port=5000 by default
```
python api.py --run
```

### Start the API with Docker
#### Build the image first
```
docker build -t flask-movie-api .
```
#### Start the service
```
docker run -it  -p 5000:5000 flask-movie-api
```

### Start the API with Docker
#### Option 1: v1 branch of the docker/compose repo
```
docker-compose up
```
#### Option 2: v2 branch of the docker/compose repo
```
docker compose up
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

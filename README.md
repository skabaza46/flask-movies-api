# flask-movies-api
A Flask API Serving movie data

## Setup Instructions
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
python init_db.py
```

### Start the API
#### Runt below command, starts at port=5000 by default
```
python api.py
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

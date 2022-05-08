## Running the project:

start the backend:
	gunicorn backend.gunicorn:application

run tests:
	python test.py


## API
### STARTING THE PROJECT
- using docker: run `docker-compose up --build`, the project will start and database migration will be triggered automatically
- navigate to [MoviesAPI](http://localhost:8000/)
to see all the endpoints
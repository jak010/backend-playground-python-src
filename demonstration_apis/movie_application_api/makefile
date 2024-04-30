

app.docker.up:
	docker-compose -f ./.docker/docker-compose.yml up --remove-orphans

app.docker.down:
	docker-compose -f ./.docker/docker-compose.yml down --remove-orphans

app.local:
	uvicorn application:application --reload

app.dev:
	uvicorn application:application --workers=4 --limit-concurrency=100000 --backlog=2048 --factory


app.guicorn:
	gunicorn application:application --worker-class uvicorn.workers.UvicornWorker -w 4 --preload --bind 0.0.0.0:8000 --reload


orm.model:
	sqlacodegen mysql+pymysql://root:1234@localhost:18001/movie_app_db > ./adapter/database/orm.py


# test

load.test.post:
	locust -f ./test/locust/member_router.py --host=http://127.0.0.1:8000 --processes 4

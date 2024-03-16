
app.docker.up:
	docker-compose -f ./.docker/docker-compose.yml up --remove-orphans


app.docker.down:
	docker-compose -f ./.docker/docker-compose.yml down

app.local:
	uvicorn application:demoapplication --reload

app.dev:
	uvicorn application:demoapplication --workers 4

app.guicorn:
	gunicorn application:demoapplication --worker-class uvicorn.workers.UvicornWorker -w 8 --keep-alive 60 --preload --bind 0.0.0.0:8000

# ORM

orm.model:
	sqlacodegen mysql+pymysql://root:1234@localhost:19501/demo > ./src/orm.py

orm.model.tables:
	sqlacodegen --noclasses mysql+pymysql://root:1234@localhost:19501/demo > ./src/orm.py


# Test Command
load.test.post:
	locust -f ./load-test/load-test-increase-like-post.py --host=http://127.0.0.1:8000 --processes 5


app.docker.up:
	docker-compose -f ./.docker/docker-compose.yml up --remove-orphans


app.docker.down:
	docker-compose -f ./.docker/docker-compose.yml down

app.local:
	uvicorn application:demoapplication --reload

app.dev:
	uvicorn application:demoapplication --workers 4

app.guicorn:
	gunicorn application:demoapplication --worker-class uvicorn.workers.UvicornWorker -w 4  --preload --bind 0.0.0.0:8000 --reload

# ORM

orm.model:
	sqlacodegen mysql+pymysql://root:1234@localhost:19501/demo > ./src/orm.py

orm.model.tables:
	sqlacodegen --noclasses mysql+pymysql://root:1234@localhost:19501/demo > ./src/orm.py


load.test.post:
	locust -f ./tests/locust/proxy_sql_test.py --host=http://127.0.0.1:8000 --processes 4

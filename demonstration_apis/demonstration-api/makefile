
app.docker:
	docker-compose -f ./.docker/docker-compose.yml up --remove-orphans

app.local:
	uvicorn application:demoapplication --reload

app.dev:
	uvicorn application:demoapplication --workers 4

# ORM

orm.model:
	sqlacodegen mysql+pymysql://root:1234@localhost:19501/demo > ./src/orm.py

orm.model.tables:
	sqlacodegen --noclasses mysql+pymysql://root:1234@localhost:19501/demo > ./src/orm.py


# Test Command
load.test.v1:
	locust -f ./load-test/load-test-v1.py --host=http://127.0.0.1:8000 --processes 3

load.test.v2:
	locust -f ./load-test/load-test-v2.py --host=http://127.0.0.1:8000 --processes 3

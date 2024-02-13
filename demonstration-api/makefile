

app.docker:
	docker-compose -f ./.docker/docker-compose.yml up --remove-orphans

app.dev:
	uvicorn application:demoapplication --reload

# Test Command
load.test:
	locust -f ./load-test/load-test-v1.py --host=http://127.0.0.1:8000 --processes 3
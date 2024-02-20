

app.docker:
	docker-compose -f ./.docker/docker-compose.yml up --remove-orphans

app.local:
	uvicorn application:pubsub_application --reload

app.dev:
	uvicorn application:pubsub_application --workers 4
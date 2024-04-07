

app.docker.up:
	docker-compose -f ./.docker/docker-compose.yml up --remove-orphans

app.docker.down:
	docker-compose -f ./.docker/docker-compose.yml down --remove-orphans

app.local:
	uvicorn application:application --reload

app.dev:
	uvicorn application:application --workers 4
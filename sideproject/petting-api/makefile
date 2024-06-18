

# Container

app.docker.up:
	docker-compose -f ./.docker/docker-compose.yml up
app.docker.down:
	docker-compose -f ./.docker/docker-compose.yml down

# Application Execute Commandx

app.local:
	uvicorn src.application:PettingApplication --host 0.0.0.0 --reload

app.dev:
	uvicorn src.application:PettingApplication --workers 4


# Configure

orm.model:
	sqlacodegen --outfile ./adapter/database/orm.py mysql+pymysql://root:1234@localhost:9100/pettingdb

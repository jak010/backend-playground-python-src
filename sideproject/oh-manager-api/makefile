run.local:
	uvicorn src.application:Application --host 0.0.0.0 --port 8000 --factory --reload

run.workers:
	uvicorn src.app:Application --host 0.0.0.0 --port 8001 --workers 4

run.gunicorn:
	gunicorn --bind 0:8000 src.app:Application --worker-class uvicorn.workers.UvicornWorker --workers 2

run.docker:
	sudo docker-compose -f ./.docker/docker-compose.yml up

orm:
	sqlacodegen mysql+pymysql://root:1234@localhost:9901/ohmanager > ./adapter/database/orm_load.py
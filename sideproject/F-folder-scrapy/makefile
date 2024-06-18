
# 개발서버용
run.dev:
	uvicorn src.app:server --host 0.0.0.0 --port 80 --factory

run.local:
	uvicorn src.app:server --host 0.0.0.0 --port 8001 --factory --reload

run.local.workers:
	uvicorn src.app:Application --host 0.0.0.0 --port 8001 --workers 4

run.gunicorn:
	gunicorn --bind 0:8000 src.app:Application --worker-class uvicorn.workers.UvicornWorker --workers 2

run.docker:
	sudo docker-compose -f ./devcontainer/docker-compose.yml up


orm:
	sqlacodegen mysql+pymysql://root:1234@localhost:9901/folder > ./src/adapter/database/orm2.py

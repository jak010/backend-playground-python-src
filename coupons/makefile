
orm:
	sqlacodegen mysql+pymysql://root:1234@localhost:9501/coupons > ./config/orm.py

# local

run.local:
	uvicorn application:coupon_issurance_application --reload

run.local2:
	uvicorn application:coupon_issurance_application --workers 4 --limit-concurrency 200 --timeout-keep-alive 10  --log-config ./log.ini --reload

run.gunicorn:
	gunicorn application:coupon_issurance_application --worker-class uvicorn.workers.UvicornWorker -w 20 -t 60 --max-requests 250  --max-requests-jitter 250 --preload

## Deploy

run.docker.db:
	sudo docker-compose -f ./.docker/docker-compose-db.yml up --remove-orphans

run.docker.app:
	sudo docker-compose -f ./.docker/docker-compose-db.yml up --remove-orphans

run.docker: run.docker.db run.docker.app

# Test Command
load.test:
	locust -f ./load-test/locustfile-issue-v1.py --host=http://127.0.0.1:8000 --processes 3
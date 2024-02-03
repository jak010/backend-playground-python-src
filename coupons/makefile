
orm:
	sqlacodegen mysql+pymysql://root:1234@localhost:9501/coupons > ./config/orm.py

# local

run.local:
	uvicorn application:coupon_issurance_application --log-config ./log.ini --reload


## Deploy

run.docker.db:
	sudo docker-compose -f ./.docker/docker-compose-db.yml up --remove-orphans

run.docker.app:
	sudo docker-compose -f ./.docker/docker-compose-db.yml up --remove-orphans

run.docker: run.docker.db run.docker.app

# Test Command
load.test:
	locust -f ./load-test/locustfile-issue-v1.py --host=http://127.0.0.1:8000
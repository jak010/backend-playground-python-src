
orm:
	sqlacodegen mysql+pymysql://root:1234@localhost:9501/coupons > ./config/orm.py

# local

run.local:
	uvicorn application:coupon_issurance_application --reload

run.local2:
	uvicorn application:coupon_issurance_application --workers 4 --timeout-keep-alive 10  --log-config ./log.ini --reload

run.gunicorn:
	gunicorn application:coupon_issurance_application --worker-class uvicorn.workers.UvicornWorker -w 4  -t 24 --keep-alive 60 --preload --bind 0.0.0.0:8000

run.gunicorn2:
	# https://www.uvicorn.org/deployment/#gunicorn
	gunicorn application:coupon_issurance_application -k uvicorn.workers.UvicornH11Worker -w 20 --keep-alive 10 --preload


## Deploy

run.docker.infra:
	sudo docker-compose -f ./.docker/docker-compose-infra.yml up -d --remove-orphans


# Test Command
load.test:
	locust -f ./load-test/locustfile-issue-v1.py --host=http://127.0.0.1:8000 --processes 3

load.test.async:
	locust -f ./load-test/locustfile-issueasync-v1.py --host=http://127.0.0.1:8000 --processes 3
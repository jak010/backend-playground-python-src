
orm:
	sqlacodegen mysql+pymysql://root:1234@localhost:9501/coupons > ./config/orm.py

orm.table:
	sqlacodegen tables mysql+pymysql://root:1234@localhost:9501/coupons > ./config/orm_tables.py


run.local:
	uvicorn application:coupon_issurance_application --reload

run.docker:
	sudo docker-compose -f ./.docker/docker-compose.yml up -d


load.test:
	locust -f ./load-test/locustfile-issue-v1.py --host=http://127.0.0.1:8000
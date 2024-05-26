

run.local:
	uvicorn main:application --port 8080  --reload


orm.mode:
	sqlacodegen mysql+pymysql://root:1234@127.0.0.1:19501/demo


load.test.post:
	locust -f ./test/locust-router.py --host=http://127.0.0.1:8080 --processes 4
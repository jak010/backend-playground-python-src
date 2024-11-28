

run.local.docker:
	sudo docker-compose -f .docker/docker-compose.yml up

run.local:
	uvicorn main:application --reload


patch.orm:
	sqlacodegen mysql+pymysql://root:1234@127.0.0.1:18501/legacy_dsp_db > ./orm.py


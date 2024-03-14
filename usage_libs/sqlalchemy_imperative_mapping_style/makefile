# ORM

orm.model:
	sqlacodegen mysql+pymysql://root:1234@localhost:19501/demo > ./examples/base_model.py

orm.model.tables:
	sqlacodegen --noclasses mysql+pymysql://root:1234@localhost:19501/demo > ./examples/base_model.py



# docker
app.docker:
	docker-compose -f ./.docker/docker-compose.yml up --remove-orphans
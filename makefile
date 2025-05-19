

setup.resource.infra:
	docker-compose -f ./1_resource/3_container/docker-compose.yml up -d

setup.rdb.model:
	sqlacodegen mysql+pymysql://root:1234@localhost:19501/demo

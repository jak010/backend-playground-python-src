#!/bin/bash -xe

apt update -y
apt-get install python3 -y
apt-get install -y python3-pip curl git

git clone https://github.com/jak010/fastapi-bolierplate.git

cd fastapi-bolierplate
pip3 install -r requirements.txt

uvicorn application:application --port 8000 --workers 4

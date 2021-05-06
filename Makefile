init:
	mkdir data
	python3.5 -m venv venv
	cp .env.example .env

activate:
	source ./venv/bin/activate

install:
	pip install -r requirements.txt
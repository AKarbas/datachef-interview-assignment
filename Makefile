.PHONY: start

start:
	docker-compose up -d --build

importdata: start
	cd webapp; ./manage.py importdata

test: start
	cd webapp; ./manage.py test


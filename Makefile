.PHONY: start

start:
	docker-compose up -d --build

importdata: start
	docker-compose exec campaigns_webapp ./manage.py importdata

test: start
	docker-compose exec campaigns_webapp ./manage.py test

stop:
	docker-compose stop

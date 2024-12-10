.PHONY: test initial_start clean

test:
	chmod +x scripts/test-entrypoint.sh
	docker-compose -f docker-compose.test.yml run --rm web_test tests
	docker-compose -f docker-compose.test.yml down -v --remove-orphans

initial_start:
	docker-compose build
	docker-compose run --rm web python manage.py migrate
	docker-compose run --rm web python manage.py populate_db
	docker-compose up

clean:
	docker-compose down -v --remove-orphans

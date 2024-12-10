.PHONY: test

test:
	chmod +x scripts/test-entrypoint.sh
	docker-compose -f docker-compose.test.yml up --build --quiet-pull --no-log-prefix -d
	docker-compose -f docker-compose.test.yml logs -f web_test
	docker-compose -f docker-compose.test.yml down -v
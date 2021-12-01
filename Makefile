

clean-db:
	rm -rf db-data/*

clean-all: clean-db
	docker-compose rm -f && docker image rm cryptowatch_walletwatcher || true

stop:
	docker-compose stop

start:
	docker-compose up --force-recreate --build



clean:
	docker-compose down --rmi local -v --remove-orphans

clean-all: clean
	rm -rf db-data/*

clean-soft:
	docker image rm -f cryptowatch_walletwatcher

stop:
	docker-compose stop

start:
	docker-compose up --force-recreate --build

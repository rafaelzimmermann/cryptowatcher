

clean:
	docker-compose down --rmi all -v --remove-orphans

clean-all: clean
	rm -rf db-data/*

stop:
	docker-compose stop

start:
	docker-compose up --force-recreate --build

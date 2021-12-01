

clean-db:
	rm -rf db-data/*

clean: clean-db
	docker-compose down --rmi all -v --remove-orphans

stop:
	docker-compose stop

start:
	docker-compose up --force-recreate --build


run:
	docker compose --env-file .env up -d

stop:
	docker compose stop 

reload:
	docker compose stop
	docker compose --env-file .env up -d

build:
	docker build -t courses-img .

rebuild:
	docker compose down
	docker image rm courses-api
	docker build -t courses-img .
	docker compose --env-file .env up -d 
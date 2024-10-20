
run:
	docker compose --env-file .env up -d

stop:
	docker compose stop 

reload:
	docker compose stop
	docker compose --env-file .env up -d

rebuild:
	docker compose down
	docker image rm courses-api
	docker compose --env-file .env up -d 
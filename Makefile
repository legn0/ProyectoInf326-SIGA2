SERVICE_NAME = rabbit enrollment Schedule 

build-all:
	cd courses ;\
	make build 

	cd Schedule ;\
	docker build -t schedule-img -f ./API/Dockerfile .

	cd enrollment ;\
	docker build -t enrollment-img . 

$(SERVICE_NAME): %:
	cd $* ;\
	docker compose up -d

courses:
	cd courses ;\
	make run 

run-rabbit:
	cd  rabbit ;\
	docker compose up -d

run-all:

	cd courses ;\
	make run

	cd enrollment ;\
	docker compose up -d
	
	cd Schedule ;\
	docker compose up -d
	

stop-all:
	cd courses ;\
	make stop

	cd enrollment ;\
	docker compose stop
	
	cd Schedule ;\
	docker compose stop




	

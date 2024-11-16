SERVICE_NAME = rabbit enrollment Schedule

# Construir todo
build-all:
	cd courses && make build
	cd Schedule && docker build -t schedule-img -f ./API/Dockerfile .
	cd enrollment && docker build -t enrollment-img .

# Crear servicios (usando docker-compose)
$(SERVICE_NAME): %:
	cd $* && docker compose up -d

# Construir y correr la aplicación en courses
courses:
	cd courses && make run

# Correr el servicio rabbit (usando docker-compose)
run-rabbit:
	cd rabbit && docker compose up -d

# Correr todos los servicios (courses, enrollment, Schedule)
run-all:
	cd courses && make run
	cd enrollment && docker compose up -d
	cd Schedule && docker compose up -d

# Detener todos los servicios (courses, enrollment, Schedule)
stop-all:
	cd courses && make stop
	cd enrollment && docker compose stop
	cd Schedule && docker compose stop

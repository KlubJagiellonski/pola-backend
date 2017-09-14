# Pola backend - jak programować przy użyciu Docker'a

## Docker

Install and run [Docker](https://docs.docker.com/compose/install/)

## Build docker image and start it
```
docker-machine start docker-vm
eval "$(docker-machine env docker-vm)"
make build
./utils/docker_run.sh 
```
This command will block the terminal. Please use another terminal for further steps.
## Create db in database container
```
createdb pola -h localhost -U postgres
```

## Set the environment variables, create the database
```
make enter
export GS1_API_KEY=KLUCZ_DO_API
export DATABASE_URL=$(echo "postgres://postgres:postgres@$POSTGRES_PORT_5432_TCP_ADDR:$POSTGRES_PORT_5432_TCP_PORT/pola")
python manage.py migrate
python manage.py createsuperuser
exit
```

## Run the Django application
```
make enter
python manage.py runserver 0.0.0.0:8000
```

## Open the Pola app in your browser
```
boot2docker ip
Open your browser at DOCKER_IP:8000
```

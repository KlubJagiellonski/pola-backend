# Pola backend - jak programować przy użyciu Docker'a

## Docker

Install and run [Docker](https://docs.docker.com/compose/install/)

## Build docker image and start it
```
make build
./utils/docker_run.sh 
```
This command will block the terminal. Please use another terminal for further steps.

## Dump current db from heroku staging (you need to request the access first)
```
./utils/dump_db_from_heroku.sh
```

## Restore the database, set the environment variables
```
make enter
cd utils
restore_db_from_dump.sh DUMP_FILENAME
cd ..
export GS1_API_KEY=KLUCZ_DO_API
export DATABASE_URL=$(echo "postgres://postgres:postgres@$POSTGRES_PORT_5432_TCP_ADDR:$POSTGRES_PORT_5432_TCP_PORT/pola")
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
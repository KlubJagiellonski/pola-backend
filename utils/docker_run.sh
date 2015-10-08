#!/usr/bin/env bash

if docker run -d --name pola-app-db postgres:9.4.1 ; then
    echo "New database created" ;
else
    echo "Starting existing database" ;
    docker start pola-app-db ;
fi

if docker run --dns 8.8.8.8 --dns 8.8.4.4 -it -v `pwd`:/app -p 2233:22 -p 8000:8000 --name pola-app-instance --link pola-app-db:postgres pola-app-image ; then
    echo "pola_instance created" ;
else
    echo "Starting existing pola instance" ;
    docker start pola-app-instance ;
fi

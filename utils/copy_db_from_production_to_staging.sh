#!/bin/sh
heroku pg:copy pola-app::HEROKU_POSTGRESQL_PURPLE blooming-gently-4582 -a pola-staging

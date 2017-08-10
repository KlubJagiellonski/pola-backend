#!/bin/sh
heroku pg:copy pola-app::DATABASE_URL DATABASE_URL -a pola-staging

# trim database on staging
# WARNING: DESTRUCTIVE ACTIONS AHEAD
# run:
# heroku run -a pola-staging
# psql $DATABASE_URL
# truncate pola_query
## truncate reversion_revision
## truncate reversion_version

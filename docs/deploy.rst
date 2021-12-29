.. contents:: :local:

Wdrażanie
---------

Możliwe jest wdrożenie aplikacji na platformę Heroku lub inną platformę wspierające `obrazy OCI <https://github.com/opencontainers/image-spec>`__/Docker.

Docker
^^^^^^

W celu zbudowania obrazu produkcyjny, ty możesz uruchomić komendę:

.. code-block:: bash

    ./scripts/prod-docker-image/build_image.sh

To powinno zbudować obraz ``docker.pkg.github.com/klubjagiellonski/pola-backend/pola-backend:latest``, który można wykorzystać do wdrożenia w środowisku kontenerowym.

Heroku
^^^^^^

Uruchom następujące polecenia, aby wdrożyć projekt w Heroku z wykorzystaniem obrazu Docker:

.. code-block:: bash

    heroku addons:create heroku-postgresql:hobby-dev
    heroku pg:backups schedule --at '02:00 America/Los_Angeles' DATABASE_URL
    heroku pg:promote DATABASE_URL

    heroku addons:create heroku-redis:hobby-dev
    heroku addons:create mailgun

    heroku config:set DJANGO_SECRET_KEY="$(openssl rand -base64 32)"
    heroku config:set DJANGO_SETTINGS_MODULE='pola.config.settings.production'

    heroku config:set POLA_APP_AWS_ACCESS_KEY_ID=YOUR_POLA_APP_AWS_ACCESS_KEY_ID_HERE
    heroku config:set POLA_APP_AWS_SECRET_ACCESS_KEY=YOUR_POLA_APP_AWS_SECRET_ACCESS_KEY_HERE
    heroku config:set POLA_APP_AWS_S3_PUBLIC_BUCKET_NAME=YOUR_POLA_APP_AWS_S3_PUBLIC_BUCKET_NAME_HERE
    heroku config:set POLA_APP_AWS_S3_BACKEND_BUCKET_NAME=YOUR_POLA_APP_AWS_S3_BACKEND_BUCKET_NAME_HERE
    heroku config:set POLA_APP_AWS_S3_AI_PICS_BUCKET_NAME=YOUR_POLA_APP_AWS_S3_AI_PICS_BUCKET_NAME_HERE

    heroku config:set DJANGO_MAILGUN_SERVER_NAME=YOUR_MALGUN_SERVER
    heroku config:set DJANGO_MAILGUN_API_KEY=YOUR_MAILGUN_API_KEY

    heroku config:set PYTHONHASHSEED=random

    ./scripts/prod-docker-image/build_image.sh
    PROD_IMAGE_NAME="docker.pkg.github.com/klubjagiellonski/pola-backend/pola-backend:latest"
    ./scripts/deploy.sh <APP_NAME> "${PROD_IMAGE_NAME}"

    heroku run python manage.py migrate
    heroku run python manage.py check --deploy
    heroku run python manage.py createsuperuser
    heroku open

Wdrożenie automatyczne
^^^^^^^^^^^^^^^^^^^^^^

Aktualnie aplikacja jest wdrażana automatycznie do dwóch śroodowisk przez Github Action. Każda zmiana w odpowiedniej gałeżi powoduje, że uruchamiany jest workflow, który testuje i buduje aplikacje.

================== =========================== ==============================================
Gałaż               Nazwa aplikacji Heroku      Adres
================== =========================== ==============================================
``master``          ``pola-app``                 ``hhttps://www.pola-app.pl/``
``prod``            ``pola-staging``             ``https://pola-staging.herokuapp.com/``
================== =========================== ==============================================

W celu wdrożęnia aplikacji z środowiska przejściowego, ty możesz wykorzystać poniższą komendę:

.. code-block:: bash

    git fetch --all
    git push origin origin/master:prod

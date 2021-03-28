Pola
==============================

.. image:: https://github.com/KlubJagiellonski/pola-backend/workflows/CI%20Build/badge.svg
     :target: https://github.com/KlubJagiellonski/pola-backend/actions
     :alt: CI Build

.. image:: https://codecov.io/gh/KlubJagiellonski/pola-backend/branch/master/graph/badge.svg?token=qh0CZKfnGR
     :target: https://codecov.io/gh/KlubJagiellonski/pola-backend
     :alt: Codedov - Coverage

.. image:: https://img.shields.io/github/issues/KlubJagiellonski/pola-backend.svg
     :target: https://github.com/KlubJagiellonski/pola-backend/issues
     :alt: GitHub issues counter

.. image:: https://img.shields.io/github/license/KlubJagiellonski/pola-backend.svg
     :alt: License

Pola pomoże Ci odnaleźć polskie wyroby. Zabierając Polę na zakupy odnajdujesz produkty “z duszą” i wspierasz polską gospodarkę.

Staging server: https://pola-staging.herokuapp.com/

LICENSE: BSD

Uruchamianie aplikacji
----------------------

Aplikacja została przygotowana do pracy w środowisku Docker. Przed pierwszym uruchomieniem musisz spełnić następujące wymagania wstępne:

1. Ty musisz mieć zainstalowane `Docker <https://docs.docker.com/get-docker/>`__:

   - Dla Linux, uruchom: ``curl https://get.docker.com | bash``
   - Dla Max OS/Windows, skorzystaj z poradnika: [Get docker](https://docs.docker.com/get-docker/)

2. Ty musisz mieć zainstalowane `docker-compose <https://docs.docker.com/compose/install/>`__:

   - Dla Linux, uruchom::

       sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

   - Dla Mac OS: Docker Desktop i Docker Toolbox zawierają już Docker Compose wraz z innymi aplikacjami Docker, więc użytkownicy nie muszą instalować Docker Compose oddzielnie.

Po wykonaniu tych kroków powiniens przygotować plik z zmiennymi środowiskowymi. Niestety niektóre komponenty wykorzystują
prywatne lub komercyjne APi, więc możesz mieć problem z dostępem, ale nie powinno to stanowić w problemu w rozwoju aplikacji.
Zmienne sa przechowywaane w pliku ``.env``. Swój zestaw zmiennych możesz stworzyć bazujac na pliku ``.env.example``.

.. code-block:: bash

    cp .env.example .env

Teraz możesz uruchomić sorodowisko:

.. code-block:: bash

    docker-compose up

Poczatkowo baza jest pusta, wiec konieczne jest przeprowadzenie migracji:

.. code-block:: bash

    docker-compose run web migrate

Zapełnij baze danych przykładowymi danymi:

.. code-block:: bash

    docker-compose run web ./manage.py populate_db

Warto również utworzyć konto administratora w systemie:

.. code-block:: bash

    docker-compose run web createsuperuser --username admin --email admin@example.org

Uruchomi to komendę interaktywną, która będzie oczekiwać podania hasła od użytkownika. Możę to wyglądać następująco.


.. code-block:: console

    $ docker-compose run web createsuperuser --username admin --email admin@example.org
    Creating pola-backend_web_run ... done
    Checking environment:
    postgres:  OK.
    Running: /app/manage.py createsuperuser --username admin --email admin@example.org
    Password:
    Password (again):
    Superuser created successfully.

Po utworzeniu konta, ty możęsz się zalogować pod adresem: http://localhost:8080/cms

Jeśli pojawi się prośba o potwierdzenia założenia konta to niezbędny link będzie dostępny w dzienniku aplikacji

.. code-block:: text

    web_1       | Content-Type: text/plain; charset="utf-8"
    web_1       | MIME-Version: 1.0
    web_1       | Content-Transfer-Encoding: 7bit
    web_1       | Subject: [example.com] Please Confirm Your E-mail Address
    web_1       | From: webmaster@localhost
    web_1       | To: admin@example.org
    web_1       | Date: Sun, 04 Oct 2020 13:51:42 -0000
    web_1       | Message-ID: <160181950227.18.15611522909315616515@17ac4ef38019>
    web_1       |
    web_1       | Hello from example.com!
    web_1       |
    web_1       | You're receiving this e-mail because user admin has given yours as an e-mail address to connect their account.
    web_1       |
    web_1       | To confirm this is correct, go to http://localhost:8080/accounts/confirm-email/MQ:1kP4QQ:okaOy8Z-KcMpSD0xSGgxPLFA2b0/
    web_1       |
    web_1       | Thank you from example.com!
    web_1       | example.com
    web_1       | -------------------------------------------------------------------------------

Ustawienia
----------

Aplikacja w dużym stopniu polegają na zmiennych środowiskowych. Został pomyślnie wdrożony zarówno z Gunicorn.

Na potrzeby konfiguracji poniższa tabela odwzorowuje zmienne środowiskowe na ich ustawienia w Django:

======================================= =========================== ============================================== ======================================================================
Zmienna środowiskowa                    Ustawienia Django           Domyślna wartośc - dewlopment                  Domyślna wartość - produkcja
======================================= =========================== ============================================== ======================================================================
DJANGO_CACHES                           CACHES (default)            locmem                                         redis
DJANGO_DATABASES                        DATABASES (default)         See code                                       See code
DJANGO_DEBUG                            DEBUG                       True                                           False
DJANGO_SECRET_KEY                       SECRET_KEY                  CHANGEME!!!                                    raises error
DJANGO_SECURE_BROWSER_XSS_FILTER        SECURE_BROWSER_XSS_FILTER   n/a                                            True
DJANGO_SECURE_SSL_REDIRECT              SECURE_SSL_REDIRECT         n/a                                            True
DJANGO_SECURE_CONTENT_TYPE_NOSNIFF      SECURE_CONTENT_TYPE_NOSNIFF n/a                                            True
DJANGO_SECURE_FRAME_DENY                SECURE_FRAME_DENY           n/a                                            True
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS   HSTS_INCLUDE_SUBDOMAINS     n/a                                            True
DJANGO_SESSION_COOKIE_HTTPONLY          SESSION_COOKIE_HTTPONLY     n/a                                            True
DJANGO_SESSION_COOKIE_SECURE            SESSION_COOKIE_SECURE       n/a                                            False
DJANGO_DEFAULT_FROM_EMAIL               DEFAULT_FROM_EMAIL          n/a                                            "pola <noreply@pola.pl>"
DJANGO_SERVER_EMAIL                     SERVER_EMAIL                n/a                                            "pola <noreply@pola.pl>"
DJANGO_EMAIL_SUBJECT_PREFIX             EMAIL_SUBJECT_PREFIX        n/a                                            "[pola] "
======================================= =========================== ============================================== ======================================================================

W poniższej tabeli wymieniono ustawienia i ich wartości domyślne dla aplikacji innych firm:

======================================= =========================== ============================================== ======================================================================
Zmienna środowiskowa                    Ustawienia Django           Domyślna wartośc - dewlopment                  Domyślna wartość - produkcja
======================================= =========================== ============================================== ======================================================================
DJANGO_AWS_ACCESS_KEY_ID                AWS_ACCESS_KEY_ID           n/a                                            <zgłasza wyjątek>
DJANGO_AWS_SECRET_ACCESS_KEY            AWS_SECRET_ACCESS_KEY       n/a                                            <zgłasza wyjątek>
DJANGO_AWS_STORAGE_BUCKET_NAME          AWS_STORAGE_BUCKET_NAME     n/a                                            <zgłasza wyjątek>

DJANGO_MAILGUN_API_KEY                  MAILGUN_ACCESS_KEY          n/a                                            <zgłasza wyjątek>
DJANGO_MAILGUN_SERVER_NAME              MAILGUN_SERVER_NAME         n/a                                            <zgłasza wyjątek>
======================================= =========================== ============================================== ======================================================================

Wdrażanie
---------

Możliwe jest wdrożenie aplikacji na platformę Heroku lub inną platformę wspierające `obrazy OCI <https://github.com/opencontainers/image-spec>`__/Docker.

Docker
^^^^^^

W celu zbudowania obrazu produkcyjny, ty możesz uruchomić komendę:

.. code-block:: bash

    ./scripts/prod-docker-image.sh

To powinno zbudować obraz ``docker.pkg.github.com/klubjagiellonski/pola-backend/pola-backend:latest``, który możnaa wykorzystać do wdorżenia na inną platfomre.

Heroku
^^^^^^

Uruchom następujące polecenia, aby wdrożyć projekt w Heroku z wykorzystaniem obrazu Docker:

.. code-block:: bash

    heroku addons:create heroku-postgresql:hobby-dev
    heroku pg:backups schedule --at '02:00 America/Los_Angeles' DATABASE_URL
    heroku pg:promote DATABASE_URL

    heroku addons:create heroku-redis:hobby-dev
    heroku addons:create mailgun

    heroku config:set DJANGO_SECRET_KEY=$(openssl rand -base64 32)
    heroku config:set DJANGO_SETTINGS_MODULE='pola.config.settings.production'

    heroku config:set DJANGO_AWS_ACCESS_KEY_ID=YOUR_AWS_ID_HERE
    heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY_HERE
    heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME=YOUR_AWS_S3_BUCKET_NAME_HERE

    heroku config:set DJANGO_MAILGUN_SERVER_NAME=YOUR_MALGUN_SERVER
    heroku config:set DJANGO_MAILGUN_API_KEY=YOUR_MAILGUN_API_KEY

    heroku config:set PYTHONHASHSEED=random

    ./scripts/prod-docker-image.sh
    ./scripts/deploy.sh

    heroku run python manage.py migrate
    heroku run python manage.py check --deploy
    heroku run python manage.py createsuperuser
    heroku open

Próba przed wykonywania migracji
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Jeśli wprowadzane są większe zmiany w bazie danych warto wykonać próbe wykorzystujać kopie bazy danych.

W tym celu uruchom przepływ pracy `"Migration validation"<https://github.com/KlubJagiellonski/pola-backend/actions/workflows/migration_check.yml>`__ korzystając z twojej gałęzi.

Nie jest wspieranie testowania migracji dla pull-requestów z forków. Kod musi być w naszym repozytorium.

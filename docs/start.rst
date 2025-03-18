Uruchamianie aplikacji
----------------------

Aplikacja została przygotowana do pracy w środowisku `Docker <https://docs.docker.com/get-docker/>`__, aby zainstalować Docker:

   - Dla Linux, uruchom: ``curl https://get.docker.com | bash``
   - Dla Max OS/Windows, skorzystaj z poradnika: [Get docker](https://docs.docker.com/get-docker/)

Po instalacji powinieneś przygotować plik z zmiennymi środowiskowymi. Niektóre komponenty wykorzystują
prywatne lub komercyjne API, więc możesz mieć problem z dostępem, ale nie powinno to stanowić w problemu w rozwoju aplikacji.
Zmienne sa przechowywaane w pliku ``.env``. Swój zestaw zmiennych możesz stworzyć bazujac na pliku ``.env.example``.

.. code-block:: bash

    cp .env.example .env

Teraz możesz uruchomić środowisko:

.. code-block:: bash

    docker compose up

Poczatkowo baza jest pusta, wiec konieczne jest przeprowadzenie migracji:

.. code-block:: bash

    docker compose run web migrate

Zaimportuj dane GPC

.. code-block:: bash

    docker compose run web import_gdc pola/gpc/fixtures/GPC_as_of-May_2021_GDSN_v20210723_PL.xml

Zapełnij baze danych przykładowymi danymi:

.. code-block:: bash

    docker compose run web populate_db

Warto również utworzyć konto administratora w systemie:

.. code-block:: bash

    docker compose run web createsuperuser --username admin --email admin@example.org

Uruchomi to komendę interaktywną, która będzie oczekiwać podania hasła od użytkownika. Może to wyglądać następująco.


.. code-block:: console

    $ docker compose run web createsuperuser --username admin --email admin@example.org
    Creating pola-backend_web_run ... done
    Checking environment:
    postgres:  OK.
    Running: /app/manage.py createsuperuser --username admin --email admin@example.org
    Password:
    Password (again):
    Superuser created successfully.

Po utworzeniu konta, ty możesz się zalogować pod adresem: ``http://localhost:8080/cms/``

Jeśli pojawi się prośba o potwierdzenia założenia konta to niezbędny link będzie dostępny w dzienniku aplikacji.

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

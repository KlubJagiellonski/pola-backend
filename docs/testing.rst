.. contents:: :local:

Testowanie
----------

Statyczne kontrola kodu
^^^^^^^^^^^^^^^^^^^^^^^

Statyczne weryfikacje kodu służy do sprawdzania, czy kod spełnia określone standardy jakości. Wszystkie statyczne kontrole kodu można przeprowadzić za pomocą frameworka `pre-commit <https://pre-commit.com/>`__.

Sprawdzenia pre-commit wykonują całą niezbędną instalację, gdy uruchamiasz je po raz pierwszy.

Pre-commit hooki
================

Pre-commi hooki pomagają przyspieszyć lokalny cykl rozwoju i zmniejszyć obciążenie infrastruktury CI. Rozważ zainstalowanie narzędzia pre-commit, aby uruchamiał się automatycznie dla każdego commita.

Pre-commi hooki domyślnie sprawdzają tylko pliki, nad którymi aktualnie pracujesz, co czynni je szybkimi. Każdy hook jest instalowany w osobnym śroodowisku niezależnym od systemu, a więc może być pewien, że sprawdzenia wykonane lokalne powiodą się również na środowisku CI.

Zintegrowaliśmy fantastyczne ramy pre-commit w naszym przepływie pracy programistycznej. Aby go zainstalować i używać, potrzebujesz lokalnie przynajmniej Pythona 3.6.

Instalacja pre-commit hooków
============================

Aby zainstalować haki pre-commit uruchom:

.. code-block:: bash

    pip install pre-commit
    pre-commit install

Po instalacji, podpięcia pre-commit są uruchamiane automatycznie podczas tworzenia commitów i będą działać tylko na plikach, które zmienisz w ostatnim commicie, więc zwykle są dość szybkie i nie spowalniają iteracji. Istnieją również sposoby, aby tymczasowo wyłączyć wstępne zatwierdzanie, gdy zatwierdzasz kod za pomocą przełącznika ``--no-verify`` lub pomijasz pewne sprawdzenia, które mogą znacznie zakłócać pracę.

Włączanie hooków pre-commit
===========================

Aby włączyć sprawdzanie przed zatwierdzeniem podczas tworzenia commitów w git, wpisz:

.. code-block:: bash

    pre-commit install

Aby zainstalować czeki również dla operacji pre-push, wprowadź:

.. code-block:: bash

    pre-commit install -t pre-push

Aby uzyskać szczegółowe informacje na temat zaawansowanych technik instalacji, uruchom:

.. code-block:: bash

    pre-commit install --help

Wyłączanie poszczególnych hooków
================================

Wyłączanie poszczególnych hooków

Jeśli masz problem z uruchomieniem konkretnego hooka, to możesz wyłączyć je tymczasowo. Aby to zrobić ty musisz ustawić zmienną środowiskową ``SKIP`` na listę oddzielonych przecinkami hooków do pominięcia. Na przykład, jeśli chcesz pominąć sortowanie definicji importów, powinieneś być w stanie to zrobić, ustawiając ``export SKIP=isort``. Możesz również dodać to do swojego ``.bashrc`` lub ``.zshrc``, jeśli nie chcesz ustawiać go ręcznie za każdym razem, gdy wchodzisz do terminala.

Używanie pre-commit hooków
==========================

Po instalacji, hooki pre-commit są tworzone automatycznie, gdy tworzysz commit, ale ty możesz je również uruchamiac manualnie, jesli potrzebujesz.

- Uruchom wszystkie kontrole plików umieszczonych w poczekalni (ang. staged files):

  .. code-block:: bash

      pre-commit run

- Uruchom tylko sprawdzenie ``isort`` na plikach w poczelni:

  .. code-block:: bash

      pre-commit run isort

- Uruchom tylko sprawdzenie ``isort`` na wszystkich plikach:

  .. code-block:: bash

      pre-commit run isort --all-files

- Uruchom wszystkie sprawdzenia na wszystkich plikach:

  .. code-block:: bash

      pre-commit run --all-files

- Uruchom wszystkie sprawdzenia tylko na plikach zmodyfikowanych w ostatnim dostępnym lokalnie commit w aktualnej gałęzi:

  .. code-block:: bash

      pre-commit run --source=HEAD^ --origin=HEAD

- Pomiń jedno lub więcej sprawdzeń, określając listę sprawdzeń oddzielonych przecinkami do pominięcia w zmiennej ``SKIP``:

  .. code-block:: bash

      SKIP=mypy,flake8,build pre-commit run --all-files

Zawsze możesz pominąć uruchamianie testów, podając flagę ``--no-verify`` w poleceniu ``git commit``.

Po więcej informacji na temat użycia hooków pre-commit, zobacz `Witryna Pre-commit <https://pre-commit.com/>`__.

Testy automatyczne dla Pythona
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Kod logiki jest automatycznie testowny z wykorzystaniem frameworka testowego dostarczonego przez Django. Wszystkie testy znajduja się w katalogach: ``pola/*/tests``

Aby uruchomić wszystkie test uruchom:

  .. code-block:: bash

      docker-compose run --rm web manage.py test

Możesz określić poszczególne testy do uruchomienia, dostarczając dowolną liczbę „etykiet testowych” do komendy ./manage.py. Każda etykieta testowa może być pełną kropkowaną ścieżką Pythona do pakietu, modułu, podklasy TestCase lub metody testowej. Na przykład:

  .. code-block:: bash

      # Uruchamia wszystkie testy znalezione w pakiecie pola.company
      docker-compose run --rm web ./manage.py test pola.company

      # Uruchom tylko jeden test case
      docker-compose run --rm web ./manage.py test pola.tests.test_views.TestFrontPageView

      # Uruchamia tylko jedna metode testową
      docker-compose run --rm web ./manage.py test pola.tests.test_views.TestFrontPageView.test_template_used

Możesz również podać ścieżkę do katalogu, aby wykryć testy poniżej tego katalogu:

  .. code-block:: bash

      docker-compose run --rm web ./manage.py test animals/

Więcej informacji na temat tesotwnia dostępna jest w dokumenttacji Djangoo: `Testing in Django <https://docs.djangoproject.com/pl/3.2/topics/testing/>`__.

Próba przed wykonywania migracji
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Jeśli wprowadzane są większe zmiany w bazie danych warto wykonać próbe wykorzystujać kopie bazy danych.

W tym celu `uruchom przepływ pracy <https://docs.github.com/en/actions/managing-workflow-runs/manually-running-a-workflow>`__ o nazwie `"Migration validation" <https://github.com/KlubJagiellonski/pola-backend/actions/workflows/migration_check.yml>`__ na Github Actionkorzystając z twojej gałęzi.

Nie jest wspieranie testowania migracji dla pull-requestów z forków. Kod musi być w naszym repozytorium.

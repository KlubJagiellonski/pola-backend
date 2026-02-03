.. contents:: :local:

Hostowanie strony WWW
---------------------

Warstwa WWW (publiczne strony, pliki HTML/JS/CSS itd.) jest serwowana na podstawie statycznych plików html z bucketa GCS. Aplikacja Django działa jako proxy, który wyszukuje odpowiedni obiekt w buckecie i zwraca go z prawidłowym nagłówkiem typu MIME.

Adres produkcyjny i repozytorium
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Strona produkcyjna: https://www.pola-app.pl/
- Repozytorium z zawartością strony (pola-web): https://github.com/KlubJagiellonski/pola-web
- CI/CD: w repozytorium ``pola-web`` skonfigurowane jest CD (via GitHub Actions), które po zbudowaniu strony uploaduje statyczne pliki HTML/JS/CSS do bucketa GCS wskazanego przez konfigurację. Następnie są one serwowane użytkownikom poprzez ``PolaWebView``.

Przepływ żądania
^^^^^^^^^^^^^^^^^

- Wszystkie nieznane ścieżki URL, które nie pasują do zdefiniowanych widoków (API, CMS, admin, itp.), trafiają do ``PolaWebView`` dzięki regule fallback w ``pola/config/urls.py``: ``re_path('^.*', views_pola_web.page_not_found_handler)``.
- Widok ``PolaWebView`` (``pola/views_pola_web.py``) odwzorowuje ścieżkę żądania na klucze w buckecie ``GCS_WEB_BUCKET_NAME`` i pobiera zawartość przez GCS API.
- Renderowana jest zawartość i nagłówek ``Content-Type`` zgodny z metadanymi obiektu w GCS.

Mapowanie ścieżek na pliki w GCS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Widok używa funkcji ``get_candidates`` do ustalenia listy możliwych kluczy w GCS na podstawie ``request.path``:

- ``/`` lub pusty path → ``index.html``
- Ścieżka bez rozszerzenia (katalogowa) np. ``/artykul`` lub ``/foo/bar/`` → próba w kolejności: ``artykul`` oraz ``artykul/index.html`` (analogicznie ``foo/bar`` oraz ``foo/bar/index.html``)
- Ścieżka z rozszerzeniem np. ``/assets/app.js`` → dokładnie ``assets/app.js``

Uwaga: jeśli flaga ``USE_ESCAPED_GCS_PATHS`` jest włączona i klucz zawiera ``\``, to przed odczytem z GCS backslash jest zastępowany przez ``___`` (obsługa specyficznych ścieżek w środowisku lokalnym).

Konfiguracja i zmienne środowiskowe
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``POLA_APP_GCS_WEB_BUCKET_NAME`` → ``GCS_WEB_BUCKET_NAME`` — nazwa bucketa z plikami WWW (wymagane w produkcji).
- ``POLA_APP_GCS_PUBLIC_BASE_URL`` → ``GCS_PUBLIC_BASE_URL`` — opcjonalny base URL (np. proxy/emulator).
- ``USE_ESCAPED_GCS_PATHS`` — włączone domyślnie lokalnie, wyłączone w produkcji.

Buforowanie i kompresja
^^^^^^^^^^^^^^^^^^^^^^^

Widok ma wbudowane wsparcie dla wydajności i cachowania:

- ``@gzip_page`` — automatyczna kompresja odpowiedzi GZIP po stronie Django.
- ``@condition`` — obsługa zapytań warunkowych (ETag i Last-Modified) na podstawie metadanych obiektu w GCS. Zwracane są odpowiednio kody ``304 Not Modified`` bez treści przy trafieniu warunku.
- ``@cache_page(60 * 15)`` — buforowanie odpowiedzi w cache Django przez 15 minut.
- Dodatkowo, dla dużych odpowiedzi (> 256 KB) dodawane są nagłówki „no-store/no-cache” po stronie klienta (``add_never_cache_headers``), aby przeglądarki/proxy nie utrwalały ciężkich zasobów. Serwerowe cachowanie Django może jednak nadal obowiązywać przez zadany TTL.

Obsługa błędów i wykluczeń
^^^^^^^^^^^^^^^^^^^^^^^^^^

- Ścieżki prowadzące do CMS i REST API są celowo wykluczane z mechanizmu proxy.
- Dla pozostałych ścieżek, gdy żaden kandydat nie istnieje w GCS, aplikacja próbuje zwrócić plik ``404.html`` z tego samego bucketa z kodem 404.
- Jeżeli również ``404.html`` nie istnieje, zwracana jest domyślna strona 404 Django.

Typowe scenariusze
^^^^^^^^^^^^^^^^^^

- Strona główna: żądanie ``GET /`` → GCS ``index.html``.
- Strona artykułu: ``GET /artykul`` → GCS ``artykul`` lub ``artykul/index.html``.
- Zasób statyczny: ``GET /assets/app.js`` → GCS ``assets/app.js`` z ``Content-Type: application/javascript`` (o ile taki ustawiono na obiekcie GCS).


Uwagi implementacyjne
^^^^^^^^^^^^^^^^^^^^^^

- Połączenia z GCS są tworzone przez ``pola/gcs.py`` (klient ``google-cloud-storage``).
- Widok opiera się na odczytach metadanych (``head_object``) do sprawdzania istnienia obiektu oraz odczytach ``GET`` do zwrotu treści.
- Ścieżki w GCS zawsze używają separatora ``/`` niezależnie od systemu plików hosta.
- DNS skonfigurowany jest via Cloudflare

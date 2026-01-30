.. contents:: :local:

Hostowanie strony WWW
---------------------

Warstwa WWW (publiczne strony, pliki HTML/JS/CSS itd.) jest serwowana na podstawie statycznych plików html z bucketa S3. Aplikacja Django działa jako proxy, który wyszukuje odpowiedni obiekt w buckecie i zwraca go z prawidłowym nagłówkiem typu MIME.

Adres produkcyjny i repozytorium
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Strona produkcyjna: https://www.pola-app.pl/
- Repozytorium z zawartością strony (pola-web): https://github.com/KlubJagiellonski/pola-web
- CI/CD: w repozytorium ``pola-web`` skonfigurowane jest CD (via GitHub Actions), które po zbudowaniu strony uploaduje statyczne pliki HTML/JS/CSS do bucketa S3 wskazanego przez konfigurację. Następnie są one serwowane użytkownikom poprzez ``PolaWebView``.

Przepływ żądania
^^^^^^^^^^^^^^^^^

- Wszystkie nieznane ścieżki URL, które nie pasują do zdefiniowanych widoków (API, CMS, admin, itp.), trafiają do ``PolaWebView`` dzięki regule fallback w ``pola/config/urls.py``: ``re_path('^.*', views_pola_web.page_not_found_handler)``.
- Widok ``PolaWebView`` (``pola/views_pola_web.py``) odwzorowuje ścieżkę żądania na klucze w buckecie ``AWS_STORAGE_WEB_BUCKET_NAME`` i pobiera zawartość przez S3 API.
- Renderowana jest zawartość i nagłówek ``Content-Type`` zgodny z metadanymi obiektu w S3.

Mapowanie ścieżek na pliki w S3
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Widok używa funkcji ``get_candidates`` do ustalenia listy możliwych kluczy w S3 na podstawie ``request.path``:

- ``/`` lub pusty path → ``index.html``
- Ścieżka bez rozszerzenia (katalogowa) np. ``/artykul`` lub ``/foo/bar/`` → próba w kolejności: ``artykul`` oraz ``artykul/index.html`` (analogicznie ``foo/bar`` oraz ``foo/bar/index.html``)
- Ścieżka z rozszerzeniem np. ``/assets/app.js`` → dokładnie ``assets/app.js``

Uwaga: jeśli flaga ``USE_ESCAPED_S3_PATHS`` jest włączona i klucz zawiera ``\``, to przed odczytem z S3 backslash jest zastępowany przez ``___`` (obsługa specyficznych ścieżek w środowisku lokalnym).

Konfiguracja i zmienne środowiskowe
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``POLA_APP_AWS_S3_WEB_BUCKET_NAME`` → ``AWS_STORAGE_WEB_BUCKET_NAME`` — nazwa bucketa z plikami WWW (wymagane w produkcji).
- ``POLA_APP_AWS_S3_ENDPOINT_URL`` → ``AWS_S3_ENDPOINT_URL`` — opcjonalny endpoint S3. Gdy ustawiony, połączenia idą pod wskazany adres/port.
- ``POLA_APP_AWS_ACCESS_KEY_ID`` / ``POLA_APP_AWS_SECRET_ACCESS_KEY`` — dane dostępowe używane do połączenia S3.
- ``USE_ESCAPED_S3_PATHS`` — włączone domyślnie lokalnie, wyłączone w produkcji.

Buforowanie i kompresja
^^^^^^^^^^^^^^^^^^^^^^^

Widok ma wbudowane wsparcie dla wydajności i cachowania:

- ``@gzip_page`` — automatyczna kompresja odpowiedzi GZIP po stronie Django.
- ``@condition`` — obsługa zapytań warunkowych (ETag i Last-Modified) na podstawie metadanych obiektu w S3. Zwracane są odpowiednio kody ``304 Not Modified`` bez treści przy trafieniu warunku.
- ``@cache_page(60 * 15)`` — buforowanie odpowiedzi w cache Django przez 15 minut.
- Dodatkowo, dla dużych odpowiedzi (> 256 KB) dodawane są nagłówki „no-store/no-cache” po stronie klienta (``add_never_cache_headers``), aby przeglądarki/proxy nie utrwalały ciężkich zasobów. Serwerowe cachowanie Django może jednak nadal obowiązywać przez zadany TTL.

Obsługa błędów i wykluczeń
^^^^^^^^^^^^^^^^^^^^^^^^^^

- Ścieżki prowadzące do CMS i REST API są celowo wykluczane z mechanizmu proxy.
- Dla pozostałych ścieżek, gdy żaden kandydat nie istnieje w S3, aplikacja próbuje zwrócić plik ``404.html`` z tego samego bucketa z kodem 404.
- Jeżeli również ``404.html`` nie istnieje, zwracana jest domyślna strona 404 Django.

Typowe scenariusze
^^^^^^^^^^^^^^^^^^

- Strona główna: żądanie ``GET /`` → S3 ``index.html``.
- Strona artykułu: ``GET /artykul`` → S3 ``artykul`` lub ``artykul/index.html``.
- Zasób statyczny: ``GET /assets/app.js`` → S3 ``assets/app.js`` z ``Content-Type: application/javascript`` (o ile taki ustawiono na obiekcie S3).


Uwagi implementacyjne
^^^^^^^^^^^^^^^^^^^^^^

- Połączenia z S3 są tworzone przez ``pola/s3.py`` (klient boto3). Jeśli ustawiono ``AWS_S3_ENDPOINT_URL``, klient używa tego endpointu (np. MinIO w docker-compose), w przeciwnym razie łączy się z AWS.
- Widok opiera się na wywołaniach ``HEAD`` (``head_object``) do sprawdzania istnienia obiektu oraz odczytach ``GET`` (``get_object``) do zwrotu treści.
- Ścieżki w S3 zawsze używają separatora ``/`` niezależnie od systemu plików hosta.
- DNS skonfigurowany jest via Cloudflare

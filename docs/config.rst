Ustawienia
----------

Aplikacja w dużym stopniu polegają na zmiennych środowiskowych.

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

======================================= ======================================= ============================================== ======================================================================
Zmienna środowiskowa                    Ustawienia Django                       Domyślna wartośc - dewlopment                  Domyślna wartość - produkcja
======================================= ======================================= ============================================== ======================================================================
POLA_APP_AWS_ACCESS_KEY_ID              AWS_ACCESS_KEY_ID                       n/a                                            <zgłasza wyjątek>
POLA_APP_AWS_SECRET_ACCESS_KEY          AWS_SECRET_ACCESS_KEY                   n/a                                            <zgłasza wyjątek>
POLA_APP_AWS_S3_PUBLIC_BUCKET_NAME      AWS_STORAGE_BUCKET_NAME                 n/a                                            <zgłasza wyjątek>
POLA_APP_AWS_S3_WEB_BUCKET_NAME         AWS_STORAGE_WEB_BUCKET_NAME             n/a                                            <zgłasza wyjątek>
POLA_APP_AWS_S3_BACKEND_BUCKET_NAME     AWS_STORAGE_BACKEND_BUCKET_NAME         n/a                                            <zgłasza wyjątek>
POLA_APP_AWS_S3_AI_PICS_BUCKET_NAME     AWS_STORAGE_AI_PICS_BUCKET_NAME         n/a                                            <zgłasza wyjątek>
POLA_APP_GET_RESPONSE_API_TOKEN         GET_RESPONSE['API_KEY']                 n/a                                            <zgłasza wyjątek>
POLA_APP_GET_RESPONSE_CAMPAIGN_ID       GET_RESPONSE['CAMPAIGN_ID']             n/a                                            <zgłasza wyjątek>
DJANGO_MAILGUN_API_KEY                  MAILGUN_ACCESS_KEY                      n/a                                            <zgłasza wyjątek>
DJANGO_MAILGUN_SERVER_NAME              MAILGUN_SERVER_NAME                     n/a                                            <zgłasza wyjątek>
======================================= ======================================= ============================================== ======================================================================

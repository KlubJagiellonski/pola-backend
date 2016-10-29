Install Certbot (https://certbot.eff.org/#pip-other):
curl https://dl.eff.org/certbot-auto >certbot-auto
chmod a+x certbot-auto

Disable SSL:
heroku config:set DJANGO_SECURE_SSL_REDIRECT=False -a pola-app


./certbot-auto certonly -d www.pola-app.pl -m koduj-z-kj@googlegroups.com --manual --debug --agree-tos --manual-public-ip-logging-ok

modify pola/urls.py according to instructions

sudo cp /etc/letsencrypt/live/www.pola-app.pl/* .

heroku certs:update fullchain.pem privkey.pem -a pola-app --confirm pola-app

heroku config:set DJANGO_SECURE_SSL_REDIRECT=True -a pola-app

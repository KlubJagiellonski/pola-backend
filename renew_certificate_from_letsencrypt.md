Install Certbot (https://certbot.eff.org/#pip-other):
curl https://dl.eff.org/certbot-auto >certbot-auto
chmod a+x certbot-auto

./certbot-auto certonly -d www.pola-app.pl -m koduj-z-kj@googlegroups.com --manual --debug --agree-tos --manual-public-ip-logging-ok --preferred-challenges dns

sudo cp /etc/letsencrypt/live/www.pola-app.pl/fullchain.pem .
sudo cp /etc/letsencrypt/live/www.pola-app.pl/privkey.pem .

heroku certs:update fullchain.pem privkey.pem -a pola-app --confirm pola-app


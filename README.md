# mastodontool
A tool intended to aid users in picking the most suitable Mastodon instance

[TOC]

## Deployment / Installation

1. Create a service user for this
```shell
sudo useradd -c "Service user for the mastodontool web app" --create-home --shell "/bin/bash" --user-group service_mastodontool
```

2. Clone this repo to your server
```shell
git clone https://gitlab.com/MaxValue/mastodontool.git
```

3. Create virtual environment in the root dir of the cloned project
```shell
python3 -m venv .venv
```

4. Install Python dependencies into the virtual environment
```shell
source .venv/bin/activate
pip install --upgrade pip
pip install --upgrade wheel
pip install --requirement requirements.txt
```

5. Create database and database user
```shell
sudo -u postgres createuser --createdb --pwprompt --createrole service_mastodontool
sudo -u postgres createdb  --owner=service_mastodontool
```

6. Fill in database connection info
```shell
# vim mastodontool/mastodontool/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'service_mastodontool',
        'USER': 'service_mastodontool',
        'PASSWORD': 'PUTYOURPASSWORDHERE',
        'HOST': 'localhost',
    }
}
```

6. Apply migrations
```shell
cd mastodontool
python3 manage.py migrate
```

7. Configure NGINX
```shell
# got to the root dir:
cd ..
sudo cp util/nginx.conf /etc/nginx/sites-available/mastodontool.conf
# fill in the domain for your server:
sudo vim /etc/nginx/sites-available/mastodontool.conf
sudo ln -s /etc/nginx/sites-available/mastodontool.conf /etc/nginx/sites-enabled/mastodontool.conf
sudo systemctl restart nginx
sudo certbot --nginx -d YOURDOMAINHERE
```

8. Install service files
```shell
sudo cp util/mastodontool.{service,socket} /etc/systemd/system/
sudo cp util/mastodontool-crawler-uptime.{service,timer} /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now mastodontool.socket
sudo systemctl enable mastodontool.timer
```

## Extending

This is a Django web app which uses Dash (Plotly) to visualize the collected data.

There are also 2 simple webcrawlers using the Python scrapy framework to gather the raw data.

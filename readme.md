# Welcome to the Ninja Mark!

this project is about making some notes and marks...

http://markninja.ru/


# Fast commands

    cd /root/list/
    source /root/list/env/bin/activate
    nano /root/list/docker-compose.yml
    nano /root/list/Dockerfile
    nano /root/list/main_files/urls.py
    nano /root/list/main_files/secret_settings.py
    
    docker-compose build
    docker-compose up --build
    docker-compose run web python manage.py createsuperuser.


# Разворачивание проекта

git clone git@gitlab.com:Kusko/list.git


# Запуск сервера

## Обновление установщика

    sudo apt-get update
    sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib nginx -y


### Create PostgreSQL Database and User (battle server only)

    **TOP SECRET**


### Create a Python Virtual Environment for your Project

    pip install --upgrade pip
    sudo pip install virtualenv
    mkdir /root/list/
    cd /root/list/
    sudo apt-get install python3.6
    virtualenv -p python3 env
    cd /root/list/
    source /root/list/env/bin/activate
    easy_install django
    pip install gunicorn
    apt-get install python3-dev
    pip install psycopg2


### Create static and media folders (battle server only)

    mkdir /opt/
    sudo rm -r -f /opt/list/static
    mkdir /opt/list/
    mkdir /opt/list/static
    mkdir /opt/list/media
    mkdir /opt/list/media/cache
    chmod -R 777 /opt
    

### Static (battle server only)

    cd /root/list/
    source /root/list/env/bin/activate
    pip install -r requirements.txt
    chmod -R 777 /root/list/manage.py
   
    ./manage.py collectstatic
    ./manage.py collectstatic --no-default-ignore
    
### Migrations, Superuser

    ./manage.py migrate --noinput
    ./manage.py createsuperuser
    123qweasd@mail.ru
    123qweasd


### Check runserver (battle server only)
! Static does not work yet

    cd /root/list/
    source /root/list/env/bin/activate
    ./manage.py runserver 0.0.0.0:8000
    
    >>> Welcome to nginx! или Стандартный ответ джанки на сайте, перейти на asphere.online:8000
.

    gunicorn --bind 0.0.0.0:8000 main_files.wsgi:application
    
    >>> Welcome to nginx! или Стандартный ответ джанки на сайте, перейти на asphere.online:8000
    

### Nginx (battle server only)
deactivate

cd /etc/nginx/sites-available

sudo nano /etc/nginx/sites-available/list

    upstream 95.213.191.108 {
        server localhost:8000 fail_timeout=0;
    }
    server {
        listen 80;
        server_name 95.213.191.108;
        return 301 http://95.213.191.108$request_uri;
    }
    server {
        listen 80;
        server_name 95.213.191.108;
        location /static/ {
            root /opt/list/;
        }
        location /media/ {
            root /opt/list/;
        }
        location / {
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_redirect off;
            proxy_pass http://95.213.191.108;
        }
    }

Copy link to main Nginx file

    sudo ln -s /etc/nginx/sites-available/list /etc/nginx/sites-enabled
    Тест nginx
    sudo nginx -t

    >>> nginx: [warn] conflicting server name "78.155.218.219" on 0.0.0.0:80, ignored
        nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
        nginx: configuration file /etc/nginx/nginx.conf test is successful

Start Nginx
    
    sudo service nginx start
    sudo service nginx restart


### Проверка статики (battle server only)
    cd /root/list
    source /root/list/env/bin/activate
    gunicorn --bind 0.0.0.0:8000 main_files.wsgi:application


### Supervisord (battle server only)
    deactivate
    apt-get install supervisor
    service --status-all | grep super
    >>> [ + ] supervisor
.
   
sudo nano /etc/supervisor/conf.d/list.conf

    [program:list]
    command=/root/list/env/bin/gunicorn --bind 0.0.0.0:8000 main_files.wsgi:application
    directory=/root/list
        

supervisorctl update



### CONGRATS YOU CAN START!

Mark Ninja here=============================this project is about making some notes and marks...## Fast commands```cd /root/list/source /root/list/env/bin/activatenano /root/list/docker-compose.ymlnano /root/list/Dockerfilenano /root/list/main_files/urls.pynano /root/list/main_files/secret_settings.pydocker-compose builddocker-compose up --builddocker-compose run web python manage.py createsuperuser.```# Разворачивание проектаgit clone git@gitlab.com:Kusko/list.git``# Запуск сервера## Обновление установщика```sudo apt-get updatesudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib nginx -y```# Create the PostgreSQL Database and User    psql    CREATE DATABASE list_db;    CREATE USER list_alpha_user WITH PASSWORD 'mucho_Listo_cuduro_324252';    GRANT ALL PRIVILEGES ON DATABASE list_db TO list_alpha_user;    \q    exit# Create a Python Virtual Environment for your Project    pip install --upgrade pip    sudo pip install virtualenv    mkdir /root/list/    cd /root/list/    sudo apt-get install python3.6    virtualenv -p python3 env    cd /root/list/    source /root/list/env/bin/activate    easy_install django    pip install gunicorn    apt-get install python3-dev    pip install psycopg2# Create and Configure a New Django Project    django-admin.py startproject main_files .# Adjust the Project Settingssettings    nano /root/list/main_files/settings.py```import datetimeimport osfrom .secret_settings import *if SERVER == 'LOCAL':    DEBUG = True    HOST = 'http://localhost:8000'    PROJECT_PATH = '/Users/Andrew/w_projects/list/'else:    DEBUG = False    HOST = 'http://asphere.online'    PROJECT_PATH = '/root/list/'INSTALLED_APPS = [    'django.contrib.admin',    'django.contrib.auth',    'django.contrib.contenttypes',    'django.contrib.sessions',    'django.contrib.messages',    'django.contrib.staticfiles',    'rest_framework',    'app1_accounts',    'app2_notebooks',]MIDDLEWARE = [    'django.middleware.security.SecurityMiddleware',    'django.contrib.sessions.middleware.SessionMiddleware',    'django.middleware.common.CommonMiddleware',    'django.middleware.csrf.CsrfViewMiddleware',    'django.contrib.auth.middleware.AuthenticationMiddleware',    'django.contrib.messages.middleware.MessageMiddleware',    'django.middleware.clickjacking.XFrameOptionsMiddleware',]ROOT_URLCONF = 'main_files.urls'TEMPLATES = [    {        'BACKEND': 'django.template.backends.django.DjangoTemplates',        'DIRS': [            os.path.join(BASE_DIR, 'templates')        ],        'APP_DIRS': True,        'OPTIONS': {            'context_processors': [                'django.template.context_processors.debug',                'django.template.context_processors.request',                'django.contrib.auth.context_processors.auth',                'django.contrib.messages.context_processors.messages',            ],        },    },]WSGI_APPLICATION = 'main_files.wsgi.application'AUTH_PASSWORD_VALIDATORS = [    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},]LANGUAGE_CODE = 'en-us'TIME_ZONE = 'UTC'USE_I18N = TrueUSE_L10N = TrueUSE_TZ = TrueAUTH_USER_MODEL = 'app1_accounts.User'JWT_AUTH = {    # 'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=3),}REST_FRAMEWORK = {    'DEFAULT_RENDERER_CLASSES': (        'rest_framework.renderers.JSONRenderer',        'rest_framework.renderers.BrowsableAPIRenderer',    ),    # 'DEFAULT_PARSER_CLASSES': (    #     'rest_framework.parsers.JSONParser',    # )    'DEFAULT_AUTHENTICATION_CLASSES': (        'rest_framework.authentication.SessionAuthentication',        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',        # 'rest_framework.authentication.BasicAuthentication'    ),    'DEFAULT_PERMISSION_CLASSES': (        'rest_framework.permissions.IsAuthenticated',    )}REST_FRAMEWORK = {    'DEFAULT_RENDERER_CLASSES': (        'rest_framework.renderers.JSONRenderer',        'rest_framework.renderers.BrowsableAPIRenderer',    ),    # 'DEFAULT_PARSER_CLASSES': (    #     'rest_framework.parsers.JSONParser',    # )    'DEFAULT_AUTHENTICATION_CLASSES': (        'rest_framework.authentication.SessionAuthentication',        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',        # 'rest_framework.authentication.BasicAuthentication'    ),    'DEFAULT_PERMISSION_CLASSES': (        'rest_framework.permissions.IsAuthenticated',    )}JWT_AUTH = {    # 'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=3),}```Secret settings    nano /root/list/main_files/secret_settings.py```import osSERVER = 'BATTLE'BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))SECRET_KEY = 'p^nx1qv8(&cp&(w6qp8*c-^1oh9=(orgno_2grq1h0o9ljb^r#'STATIC_URL = '/static/'STATIC_ROOT = "/opt/list/static/"STATICFILES_DIRS = [    ('', os.path.join(BASE_DIR, 'src'),),    ('', os.path.join(BASE_DIR, 'src/static'),),    ('', os.path.join(BASE_DIR, 'src/script'),),    ('', os.path.join(BASE_DIR, 'src/style'),),]MEDIA_URL = "/media/"MEDIA_ROOT = "/opt/list/media/"ALLOWED_HOSTS = [    'localhost',    '127.0.0.1',    '95.213.191.108',    '*',]DATABASES = {    'default': {        'ENGINE': 'django.db.backends.postgresql_psycopg2',        'NAME': 'list_db',        'USER': 'list_alpha_user',        'PASSWORD': 'mucho_Listo_cuduro_324252',        'HOST': 'localhost',        'PORT': '',    }}```urls    nano /root/list/main_files/urls.py```from django.conf import settingsfrom django.conf.urls import include, urlfrom django.contrib import adminfrom django.conf.urls.static import staticfrom django.contrib.staticfiles.urls import staticfiles_urlpatternsfrom rest_framework_jwt.views import obtain_jwt_tokenfrom app1_accounts.views import LibraryApiViewfrom app2_notebooks.views import *from rest_framework import routersfrom rest_framework import routersrouter = routers.SimpleRouter()router.register(r'points', PointApiView)router.register(r'notebooks', NotebookApiView)router.register(r'notes', NoteApiView)urlpatterns = [    url(r'^admin/', admin.site.urls),    url(r'^auth/token/api/', obtain_jwt_token),    url(r'^api/library/',           LibraryApiView.as_view(), name='api_libraries'),    # url(r'^api/notebooks/',         NotebookApiView.as_view(), name='api_notebooks'),    # url(r'^api/notes/',             NoteApiView.as_view(), name='api_note'),    # url(r'^/$', home, name='home_page'),    # url(r'^$', home, name='home_page'),    # url(r'^api/notebooks/',         NotebookApiView.as_view(), name='api_notebooks'),    # url(r'^api/points/(?P<pk>[0-9]+)/$', PointApiView.as_view(), name='api_note_qwe'),    # url(r'^api/points/',            PointApiView.as_view(), name='api_points'),    url(r'^notebook/(?P<notebook_id>\d+)/$', notebook, name='notebook'),    # url(r'^api/sheets/(?P<user_id>\d+)/$', ApiView.as_view(), name='notebooks'),    url(r'^api/', include((router.urls, 'app_name'), namespace='instance_name')),    # url(r'^', include('app2_notebooks.urls')),    # url(r'^', include('app1_accounts.urls')),    url(r'^', home, name='home'),]# urlpatterns += router.urlsurlpatterns += staticfiles_urlpatterns()if settings.DEBUG:    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)```# Загрузка файлов с помощью CyberDuck    ssh root@188.166.171.254загружаю все файлы кроме базы данных, окуружения, папки main_files и manage.py    /root/list/# Создание вспомогательных папок    mkdir /opt/    sudo rm -r -f /opt/list/static    mkdir /opt/list/    mkdir /opt/list/static    mkdir /opt/list/media    mkdir /opt/list/media/cache    chmod -R 777 /opt    chmod -R 777 /opt/list    chmod -R 777 /opt/list/static# Миграции, статика, Superuser    cd /root/list/    source /root/list/env/bin/activate    pip install -r requirements.txt    chmod -R 777 /root/list/manage.py    ./manage.py migrate --noinput    ./manage.py createsuperuser    a.kusko@list.ru    123kusk0akusk0    ./manage.py collectstatic    ./manage.py collectstatic --no-default-ignore# Проверка запуска сервера    cd /root/list/    source /root/list/env/bin/activate        ./manage.py runserver 0.0.0.0:8000    >>> Welcome to nginx! или Стандартный ответ джанки на сайте, перейти на asphere.online:8000        ! Статика еще не работает        gunicorn --bind 0.0.0.0:8000 main_files.wsgi:application    >>> Welcome to nginx! или Стандартный ответ джанки на сайте, перейти на asphere.online:8000        ! Статика еще не работает# Nginx    deactivate    cd /etc/nginx/sites-available    sudo nano /etc/nginx/sites-available/list    ```upstream 95.213.191.108:8000 {    server localhost:8000 fail_timeout=0;}server {    listen 80;    server_name 95.213.191.108:8000;    return 301 http://95.213.191.108$request_uri;}server {    listen 80;    server_name 95.213.191.108:8000;    location ^/static/ {        root /opt/list/;        autoindex on;        alias /opt/list/;    }    location /media/ {        root /opt/list/;    }    location / {        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;        proxy_redirect off;        proxy_pass http://95.213.191.108;    }}```Копирование ярлыка в основной nginx файл    sudo ln -s /etc/nginx/sites-available/list /etc/nginx/sites-enabled    Тест nginx    sudo nginx -t    >>> nginx: [warn] conflicting server name "78.155.218.219" on 0.0.0.0:80, ignored        nginx: the configuration file /etc/nginx/nginx.conf syntax is ok        nginx: configuration file /etc/nginx/nginx.conf test is successful        Запуск Nginx    sudo service nginx start    sudo service nginx restart# Supervisord    cd /root/list    source /root/list/env/bin/activate    apt-get install supervisor        service --status-all | grep super    >>> [ + ] supervisor         Проверка статики    ```[program:list]command=/root/list/env/bin/gunicorn --bind 0.0.0.0:8000 main_files.wsgi:applicationdirectory=/root/list    ``    supervisorctl update
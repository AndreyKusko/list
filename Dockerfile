FROM python:3
ENV PYTHONUNBUFFERED 1
ADD . /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN ./manage.py migrate
ADD . /code/

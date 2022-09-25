# pull official base image
FROM python:3.9-slim

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install psycopg2
RUN apt-get -y update \
    && apt-get -y install build-essential gcc python3-dev musl-dev \
    && apt-get -y install libpq-dev  \
    && pip install --upgrade pip setuptools \
    && pip install psycopg2

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput

# RUN if [ "$DJANGO_SUPERUSER_USERNAME" ]; then python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_USERNAME; fi

# add and run as non-root user
# RUN adduser -D emadmin
# USER emadmin

# run gunicorn
CMD gunicorn projectx_site.wsgi:application --bind 0.0.0.0:$PORT
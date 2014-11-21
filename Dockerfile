FROM ubuntudesign/python-auth

RUN apt-get update && apt-get install -y graphviz-dev

ADD . /app
WORKDIR /app

RUN pip install -r requirements/dev.txt

VOLUME /app

CMD DATABASE_URL=`echo $POSTGRES_PORT | sed "s!tcp://!postgres://postgres@!"`/postgres python manage.py runserver 0.0.0.0:8000

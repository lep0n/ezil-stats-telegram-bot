FROM python:3.10.3

WORKDIR /home

ENV TELEGRAM_API_TOKEN=""

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY *.py ./
COPY createdb.sql ./
COPY Pipfile ./
COPY Pipfile.lock ./

RUN pip install -U pip pipenv && apt update && apt install sqlite3
RUN sqlite3 database.db < createdb.sql
RUN pipenv install --deploy --ignore-pipfile

CMD ["pipenv", "run", "python", "app.py"]

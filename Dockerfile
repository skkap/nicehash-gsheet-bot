FROM python:3.8-slim 

WORKDIR /app

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --deploy --ignore-pipfile

COPY nicehash.py .
COPY newrelic.py .
COPY nicehash-account-stats-bot.py .
COPY nicehash-mining-stats-bot.py .
COPY nicehash-metrics-bot.py .

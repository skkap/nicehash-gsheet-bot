FROM python:3.8-slim 

WORKDIR /app

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --deploy --ignore-pipfile

COPY nicehash-account-stats-bot.py .
COPY nicehash-mining-stats-bot.py .

# CMD ["pipenv", "run", "python", "/app/nicehash-mining-stats-bot.py"]

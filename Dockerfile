FROM python:3.8-slim 

WORKDIR /app

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --deploy --ignore-pipfile

COPY nicehash.py .
COPY nicehash-bot.py .

CMD ["pipenv", "run", "python", "/app/nicehash-bot.py"]

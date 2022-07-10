FROM python:3.9

WORKDIR /app

RUN pip install pipenv

COPY Pipfile /app
COPY Pipfile.lock /app

RUN pipenv install

COPY . /app

ENV PORT=80

EXPOSE 80

CMD ["pipenv", "run", "prod"]


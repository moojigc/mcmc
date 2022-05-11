FROM python:3.9

WORKDIR /app
COPY . .
RUN mkdir data

RUN pip install pipenv
RUN pipenv install

ENV PORT=80

EXPOSE 80

CMD ["pipenv", "run", "prod"]

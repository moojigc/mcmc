FROM python:3.9

WORKDIR /app
COPY . .
RUN mkdir data
COPY /app/minecraft/automation.py /app/data/minecraft_automation.py

RUN pip install pipenv
RUN pipenv install

ENV PORT=80

EXPOSE 80

CMD ["pipenv", "run", "prod"]

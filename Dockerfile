FROM python:3.9

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

ENV PORT=80

EXPOSE 80

CMD ["gunicorn", "-w", "5", "server:app"]


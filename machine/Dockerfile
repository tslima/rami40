FROM  python:3.10.11-slim-bullseye

WORKDIR /app

COPY . .

RUN pip3 install .

EXPOSE 5000

ENV FLASK_APP=machine

RUN flask init-db

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]


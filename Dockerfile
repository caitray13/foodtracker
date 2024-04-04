FROM python:3.9

WORKDIR /code
COPY ./requirements.txt .
COPY ./foodtracker .

RUN pip install -r requirements.txt

CMD [ "python", "./app.py" ]
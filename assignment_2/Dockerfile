FROM python:3.9-slim

WORKDIR /app

COPY ./mocker_flight_service.py /app/
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

EXPOSE 8000

CMD ["python", "mocker_flight_service.py"]
FROM python:3.8

# Install packages
COPY /kafka-producer/requirements.txt ./
RUN pip3 install -r requirements.txt

COPY /kafka-producer/ /app/
WORKDIR /app
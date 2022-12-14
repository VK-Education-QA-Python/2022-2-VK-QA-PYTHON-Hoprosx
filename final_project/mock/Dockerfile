FROM python:3.10-alpine
WORKDIR /mock

COPY requirements.txt /mock
RUN pip3 install --upgrade pip -r requirements.txt

COPY ../../../vk/mock /mock

EXPOSE 5000
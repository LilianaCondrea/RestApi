FROM python:3.10.4

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir "code"
WORKDIR /code
COPY ./requirements.txt /code/

RUN pip3 install pip --upgrade
RUN pip3 install -r requirements.txt

COPY . /code/

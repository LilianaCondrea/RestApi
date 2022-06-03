FROM python:3.10.4

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir "code"

WORKDIR /code
ADD ./requirements.txt /code/

RUN pip3 install pip --upgrade
RUN pip3 install -r requirements.txt


CMD python3 manage.py makemigrations --noinput && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --noinput && \
    gunicorn Config.wsgi --bind 0.0.0.0:8000


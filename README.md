# **Blog API DRF + JWT**
A blog project with jwt authentication written by Django and DjangoRestFrameWork.<br>
Auth API has users registration, login and obtaining JWT and refreshing JWT.<br>

## Why JWT?<br>
JWTs are a good way of securely transmitting information between parties because they can be signed, which means you can be sure that the senders are who they say they are !<br>

## Permissions
- Each `User` can change only own data.<br>
- Only account's owner can view account details.<br>

---

## Clone project
```sh
$ git clone https://github.com/iarsham/RestApi-Blog.git
```
---

## install Docker
https://docs.docker.com/engine/install/
## install Docker Compose
https://docs.docker.com/compose/install/

---

# Build and run Project
```sh
$ cd RestApi-Blog/
$ docker-compose up --build 
```

# Create Superuser to access Admin Panel
```sh
$ docker-compose exec web python manage.py createsuperuser
```

---

## Technologies used

* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [DjangoRestFrameWork](https://www.django-rest-framework.org/)
* [PostgreSQL](https://www.postgresql.org/)
* [gunicorn](https://gunicorn.org/)
* [Docker](https://www.docker.com/)
* [Nginx](https://www.nginx.com/)
* [JwtAuthentication](https://jwt.io/)

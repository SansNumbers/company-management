# Company Management System

System for managing employees in the company.
The service will allow clients to register and conduct management of the company, 
its offices, employees, vehicle fleet of this companies. 
The implementation should be using python3 + django + django-rest-framework, VCS git, use as a database PostgreSQL, 
and to deploy the project - docker compose.

## Getting started

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/SansNumbers/company-management.git
$ cd company-management
```

## Install using Docker-Compose

You need to install following software beforehand:
* [Docker](https://docs.docker.com/install/)
* [Docker-compose](https://docs.docker.com/compose/install/)

Docker version must be 20.10.5 or higher.
Docker-compose version must be 1.29.0 or higher.

* Check `.env` file exists and has correct ENV values
* `docker-compose build` to build a docker image
* `docker-compose up` to run docker images
* `docker-compose run web python manage.py makemigrations` to make migrations

## To access admin panel

Navigate to `http://0.0.0.0:8000/admin/`.

## To access API Documentation

Navigate to `http://0.0.0.0:8000/swagger/` or `http://0.0.0.0:8000/redoc/`.

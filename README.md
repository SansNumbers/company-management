# Python skillup

Python skillup project

## Getting started

The first thing to do is to clone the repository:

```sh
$ git clone https://gitlab.mobidev.biz/antypin/python-skillup.git
$ cd python-skillup
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

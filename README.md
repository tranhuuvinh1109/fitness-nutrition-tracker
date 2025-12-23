# Flask API REST Template

[![Development](https://github.com/vectornguyen76/flask-rest-api-template/actions/workflows/development_pipeline.yml/badge.svg)](https://github.com/vectornguyen76/flask-rest-api-template/actions/workflows/development_pipeline.yml)
[![Staging](https://github.com/vectornguyen76/flask-rest-api-template/actions/workflows/staging_pipeline.yml/badge.svg)](https://github.com/vectornguyen76/flask-rest-api-template/actions/workflows/staging_pipeline.yml)
[![Production](https://github.com/vectornguyen76/flask-rest-api-template/actions/workflows/production_pipeline.yml/badge.svg)](https://github.com/vectornguyen76/flask-rest-api-template/actions/workflows/production_pipeline.yml)

<p align="center">
<img src="./assets/logo.png" alt="Logo" />
</p>

Rest API template developed in Python with the Flask framework. The template covers user management, jwt tokens for authentication, and assign permissions for each user with Flask Principal. In the local environment, it uses docker to create an environment made up of several services such as api (flask), database (postgresql), reverse-proxy (nginx).

## Index

- [Technology](#technology)
- [Requirements](#requirements)
- [Environments](#environments)
  - [Develop](#develop)
  - [Testing](#testing)
  - [Local](#local)
  - [Production](#production)
- [Flask Commands](#flask-commands)
  - [Flask-cli](#flask-cli)
- [Database commands](#bbdd-commands)
  - [Flask-migrate](#flask-migrate)
- [Swagger](#swagger)
- [Reference](#reference)
- [Contribution](#contribution)

## Technology

- **Operating System:** Ubuntu
- **Web Framework:** Flask
- **ORM:** Flask-sqlalchemy
- **Swagger:** Swagger-UI
- **Authentication:** Flask Json Web Token
- **Permission:** JWT Decorator
- **Serialization, Deserialization and Validation:** Marshmallow
- **Migration Database:** Flask-migrate
- **Environment manager:** Anaconda/Miniconda
- **Containerization:** Docker, docker-compose
- **Database:** PostgreSQL
- **Python WSGI HTTP Server:** Gunicorn
- **Proxy:** Nginx
- **Tests:** Unittest
- **Deployment platform:** AWS
- **CI/CD:** Github Actions

## Requirements

- [Python](https://www.python.org/downloads/)
- [Anaconda/Miniconda](instructions/anaconda-miniconda.md)
- [Docker](instructions/docker-dockercompose.md)
- [Docker-Compose](instructions/docker-dockercompose.md)
- [Github](https://github.com)

## Environments

### Develop

Development environment that uses PostgreSQL in local and uses the server flask in debug mode.

**Create environment and install packages (RUN)**

```shell
python -m venv venv

venv\Scipts\activate

pip install -r requirements.txt

# RUN

flask run

```

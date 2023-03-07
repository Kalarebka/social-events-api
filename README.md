# Social Events API

## Table of contents
* [About the project](#about-the-project)
* [Built with](#built-with)
* [Setup](#setup)
* [Usage](#usage)

## About the project


Backend Django Rest Framework API for managing social events.

Features:
* creating and managing social events
* private and group events, one-time or recurring
* user groups and friend lists
* token authentication
* app for direct messaging between users

The project contains a messagebox app to let users communicate.

<p align="right">(<a href="#top">back to top</a>)</p>


## Built With

* Django
* Django Rest Framework
* PostgreSQL
* Celery
* Redis
* Docker and Docker Compose
<p align="right">(<a href="#top">back to top</a>)</p>
    
## Setup

### Requirements:
* Docker
* Docker Compose


To run this project locally with Docker Compose:

```
$ git clone https://github.com/Kalarebka/home-manager.git
$ cd home-manager
```
Fill the .env.sample file with the required values and save as .env

```
$ docker-compose build
$ docker-compose up -d
$ docker exec -it website bash
$ python3 manage.py migrate
```
Visit localhost:8000\schema\redoc\ in the browser to see all endpoint details.

<p align="right">(<a href="#top">back to top</a>)</p>

## Usage

The API endpoints can be used with a matching frontend or accesses through an HTTP client (e.g. curl, Postman).

<p align="right">(<a href="#top">back to top</a>)</p>
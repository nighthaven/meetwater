# Meetwater

## Authors

Boris Le Bon

## install project

### 1. prerequisite

Please ensure to install:
- Docker ≥ 24
- Docker Compose ( include with Docker Desktop )

### 2. to recup the project

in the folder you want the project to be:

```shell
git clone https://github.com/nighthaven/meetwater
cd meetwater
```

### setup environnement variable

You need to create at the root of the project a file name `.env.dev`.
You should be able to see a file named `.env.template` that have an example of all the environnement variable.


## Project description

Meetwater is an application made for swimming pools.
The purpose of this application is multiple :
- Allowing people to book an appointement with a swimming coach.
- Allowing swimming coach to manage their schedules.
- Allowing swimming pool to manage their schedules and organisation.

## feed the localhost database

The scripts allowing the localhost database can be used with this terminal command

```shell
uv run python -m src.seeds.seed_all
```

## start the API

```shell
uvicorn src.main:app --reload
```

## start the tests

```shell
uv run pytest
```

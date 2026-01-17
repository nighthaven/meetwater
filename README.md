# Meetwater

## Authors

Boris Le Bon

## Project description

Meetwater is an application made for swimming pools.
The purpose of this application is multiple :
- Allowing people to book an appointement with a swimming coach.
- Allowing swimming coach to manage their schedules.
- Allowing swimming pool to manage their schedules and organisation.

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

You need to create at the root of the project a file name `.env.dev` and also a file name `.env.test`.
You should be able to see a file named `.env.template` that have an example of all the environnement variable.

## create database tables
```shell
uv run alembic upgrade head
```

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

# CDC
## Setup
After docker compose up -d

### Create slot
```bash
docker compose exec -it db psql -U ${DATABASE_USERNAME} -d ${DATABASE_NAME} -c "SELECT pg_create_logical_replication_slot('mon_slot', 'pgoutput');"
```

### Create debezium connector
```bash
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "postgres-connector",
    "config": {
      "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
      "database.hostname": "db",
      "database.port": "5432",
      "database.user": "mw",
      "database.password": "random",
      "database.dbname": "meetwater",
      "topic.prefix": "myapp",
      "table.include.list": "public.ma_table",
      "plugin.name": "pgoutput",
      "slot.name": "debezium_slot",
      "publication.name": "debezium_publication"
    }
  }'
```
Adapt values (ton_user, ton_db, public.ma_table) to your context.

### Modify debezium to listen all tables
```bash
curl -X PUT http://localhost:8083/connectors/postgres-connector/config \
  -H "Content-Type: application/json" \
  -d '{
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "db",
    "database.port": "5432",
    "database.user": "mw",
    "database.password": "random",
    "database.dbname": "meetwater",
    "topic.prefix": "myapp",
    "schema.include.list": "public",
    "plugin.name": "pgoutput",
    "slot.name": "debezium_slot"
  }'
```

### Verify connector is running
```bash
curl http://localhost:8083/connectors/postgres-connector/status
```
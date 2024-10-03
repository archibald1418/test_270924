# test_270924

### Setup instructions

- In the project's root folder create your `.env` file setting the following variables:
    - `PGUSER` - admin user for your Postgres Database
    - `PGDB` - Postgres database name
    - `PGPASS` - Postgres database password
    - `PGHOST` - Postgres database host (=container_name field)
    - `DBAPI` - Postgres driver (pg8000 or psycopg)
    - `DB` - 'postgres'

- Launch the cluster with `make` command
- The website will run at http://localhost:8000
- Documentation available at http://localhost:8000/docs

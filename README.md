# candid
Candid is a chat platform for peaceful and productive discussion of issues of public concern

# Getting Started
Download OpenAPI Generator:

`$ pip install openapi-generator-cli`

Use the generator:

`$ openapi-generator-cli generate -i docs/api.yaml -g typescript-node -o backend/src/generated`

`$ openapi-generator-cli generate -i docs/api.yaml -g javascript -o frontend/src/generated`

Host a local Swagger UI to test the API and view docs:

`$ docker pull docker.swagger.io/swaggerapi/swagger-ui`

`$ docker run -p 80:8080 -e SWAGGER_JSON=/docs/api.yaml -v ./docs:/docs/ docker.swagger.io/swaggerapi/swagger-ui`

Install the following:
* Docker Desktop 4.43.2

Run `docker compose up -d`

# Updating Python dependencies

Use the `api` container shell to update dependencies and generate a lockfile from the `/app` directory: `pip-compile requirements.in -o requirements.txt`.

# Running migrations

Use the `api` container shell to run migrations. This will delete all of your tables and data: from the `/app` directory, run `python3 database/reset_hard.py`.

Use the `api` container shell to load test data. This will do inserts without any other preparation, so you might want to run the reset script above first: from the `/app` directory, run `python3 database/load_test_data.py`.

# Accessing postgres directly

Exec into the `db` container and then run `psql --username=user mydatabase`. You can then use `psql` commands like `\l`, `\dt`, and so forth.

# TODO

* Make sure gunicorn and Flask are set up correctly for prod (eg, not running at root?)
* Set up prod vs dev Dockerfile stages so we don't copy all files to prod and such
* Set up logging
* Add rate limiting
* Set up unit tests

# Could be improved?

* Make sure gunicorn and postgres are configured to handle many long polling connections (gunicorn worker type?)
* Set up load tests
* Stop using select *
* Set up Flask config
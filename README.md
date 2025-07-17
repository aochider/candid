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

Use the `api` container to update dependencies and generate a lockfile `pip-compile requirements.in -o requirements.txt`.
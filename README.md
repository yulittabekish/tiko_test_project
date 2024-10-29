#### Run app with docker compose 
Fistly you need to create .env file in the projects root with same environment variables as provided in the .env.example file.
Secondly you can run an app using:
```shell
docker compose up --build
```
#### Migrations are applied automatically, but if you want to apply them manually you can start a container with the command from the previous section and run :
```shell
docker exec -it tiko-test-project python manage.py migrate
```

## Technologies Used

This project leverages the following technologies:

- **Django**.
- **Django REST Framework (DRF)**.
- **Django-Filter**.
- **SQLite**.
- **Docker**.
- **Docker Compose**.
- **pytest**.

## How to authorize:
Go to either **/api/register** endpoint or if you already have a user to **/api/login**:
- Provide required data:
  - username, email, password - register
  - username, password - login
- Receive access and refresh JWT tokens

Access token should be further provided in the HTTP headers in a form - "Bearer <access_token>".

## Running Tests

The application includes a `tests` folder. 
To run the tests:
```bash
pytest .
```

## API Documentation (Swagger)
Is available on the http://0.0.0.0:8000/api/schema/swagger-ui/
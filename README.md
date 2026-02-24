# MDS Energy Manager

REST API application

---

# Quick Start

Follow these steps to run the project in development mode with hot reload:

## Add `.env` file

Create a `.env` file in the project root directory  
(next to `docker-compose.yml` and `docker-compose.dev.yml`).

Use the `.env` file that was provided to the team.

️ The application will NOT start without this file because it contains required environment variables (database credentials, etc).

---

##  Start the project (Development mode)

Run:

```
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

API will be available at:

```
http://localhost:8000/api-mds
```

Application will be available at:

```
http://localhost:8000
```

---

## Stop the project

```
docker compose -f docker-compose.yml -f docker-compose.dev.yml down
```


##  Run Tests

Run tests inside the web container:

Run all the tests:
```
docker compose exec web pytest
```

Run specified file tests:
```
docker compose exec web pytest tests/integration/test_integration.py
```
Or 
```
docker compose exec web pytest tests/unit/services/test_services.py
```
Or 
```
docker compose exec web pytest tests/unit/utils/test_utils.py
```

If containers are not running, start them first:

```
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

Then run tests.
---

# Development Details

Development mode uses:

- `docker-compose.yml`
- `docker-compose.dev.yml`  
  (Django `runserver` + source code mounted into container for hot reload)

---

# Database Configuration

Postgres connection (from host machine):

- Host: `localhost`
- Port: `5433`
- Database: value from `DJ_DB_NAME`
- Username: `DJ_DB_USER`
- Password: `DJ_DB_PASSWORD`

If port `5433` is already in use, change the mapping in `docker-compose.yml`, for example:

```
"5434:5432"
```

---

# Reset Database (removes volume data)

```
docker compose -f docker-compose.yml -f docker-compose.dev.yml down -v
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

> Migrations run automatically on container startup:
>
> `python manage.py migrate --noinput`

---

# Django Management Commands

Run migrations manually:

```
docker compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py migrate
```

Create a superuser:

```
docker compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py createsuperuser
```

---

# Prerequisites

- Docker  
- Docker Compose (included with Docker Desktop)

---

**MDS Energy Manager – Development Setup**
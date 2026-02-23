# MDS Energy Manager

REST API application

---

## Prerequisites

- Docker
- Docker Compose (included with Docker Desktop)

---

## 1) Create `.env`

Create a **`.env`** file in the project root (next to `docker-compose.yml` and `docker-compose.dev.yml`).

---

## 2) Run in Development mode (hot reload)

Development uses:
- `docker-compose.yml`
- `docker-compose.dev.yml` (Django `runserver` + source code mounted into the container)

Start:

docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

Application:
- http://localhost:8000

API endpoint
- http://localhost:8000/api-mds

Postgres:
- Host: localhost
- Port: 5433
- Database: value from `DJ_DB_NAME`
- Username: `DJ_DB_USER`
- Password: `DJ_DB_PASSWORD`

Stop:

docker compose -f docker-compose.yml -f docker-compose.dev.yml down

Reset database (removes volume data):

docker compose -f docker-compose.yml -f docker-compose.dev.yml down -v  
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

> Migrations run automatically on container startup (`python manage.py migrate --noinput`).

---


## 4) Django management commands

Run migrations manually:

docker compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py migrate

Create a superuser:

docker compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py createsuperuser

---

## Notes

- If port `5433` is already in use, change the DB mapping in `docker-compose.yml` (e.g. `"5434:5432"`).
- If port `8000` is already in use, change `"8000:8000"` in `docker-compose.yml`.
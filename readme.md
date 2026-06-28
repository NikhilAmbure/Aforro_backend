````markdown
# Aforro Store Management API

A backend REST API built using **Django** and **Django REST Framework** for managing products, stores, inventory, and customer orders. This project was developed as part of a backend engineering assignment and demonstrates transactional order processing, search, Redis caching, asynchronous task processing, Docker, PostgreSQL, and automated testing.

---

# Features

- Product, Category, Store and Inventory Management
- Transaction-safe Order Processing
- Automatic Inventory Validation
- Automatic Stock Deduction
- Product Search with Multiple Filters
- Product Autocomplete Suggestions
- Pagination
- Redis Response Caching
- Celery Background Task Processing
- Swagger / OpenAPI Documentation
- Dockerized Development Environment
- PostgreSQL Database
- Dummy Data Generator
- Automated API Tests

---

# Tech Stack

- Python 3.12
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Docker & Docker Compose
- drf-spectacular (Swagger / OpenAPI)
- Faker

---

# Project Structure

```text
project/
│
├── apps/
│   ├── products/
│   ├── stores/
│   ├── orders/
│   └── search/
│
├── tests/
│
├── aforro/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
└── README.md
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/NikhilAmbure/Aforro_backend
```

---

## 2. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
SECRET_KEY=your-secret-key

DEBUG=True

DB_NAME=aforro
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

REDIS_URL=redis://redis:6379/0
```

---

## 3. Build Docker Containers

```bash
docker compose up --build
```

---

## 4. Apply Database Migrations

```bash
docker compose exec web python manage.py migrate
```

---

## 5. Generate Dummy Data

```bash
docker compose exec web python manage.py seed_data
```

The seed command generates:

- 10+ Categories
- 1000+ Products
- 20+ Stores
- Inventory for every store

---

# Docker Usage

Start all services

```bash
docker compose up
```

Stop containers

```bash
docker compose down
```

Rebuild containers

```bash
docker compose up --build
```

---

# Docker Services

Docker Compose starts the following services:

- Django Web Server
- PostgreSQL Database
- Redis
- Celery Worker

---

# Running Tests

```bash
docker compose exec web python manage.py test
```

Implemented Tests

- Order Creation (Confirmed)
- Order Creation (Rejected)
- Inventory API
- Product Search API
- Product Suggestion API

---

# Swagger / OpenAPI Documentation

Swagger UI

```
http://localhost:8000/api/docs/
```

OpenAPI Schema

```
http://localhost:8000/api/schema/
```

---

# API Endpoints

## Orders

| Method | Endpoint |
|---------|----------|
| POST | `/api/orders/` |
| GET | `/api/orders/` |

---

## Stores

| Method | Endpoint |
|---------|----------|
| GET | `/api/stores/<store_id>/inventory/` |

---

## Search

| Method | Endpoint |
|---------|----------|
| GET | `/api/search/products/` |
| GET | `/api/search/suggest/` |

---

# Sample API Requests

## Create Order

**POST**

```
/api/orders/
```

Request Body

```json
{
    "store_id": 1,
    "items": [
        {
            "product_id": 10,
            "quantity_requested": 2
        },
        {
            "product_id": 15,
            "quantity_requested": 1
        }
    ]
}
```

---

## Product Search

```
GET /api/search/products/?q=laptop
```

---

## Product Search with Filters

```
GET /api/search/products/?category=Electronics&min_price=1000&max_price=50000
```

---

## Product Suggestions

```
GET /api/search/suggest/?q=lap
```

---

## Store Inventory

```
GET /api/stores/1/inventory/
```

---

# Redis Caching

Redis is used to cache frequently requested API responses.

Currently cached endpoints include:

- Product Search API
- Product Suggestion API

Cached responses are stored for **5 minutes**, reducing repeated database queries and improving response time for frequently accessed data.

---

# Celery Background Tasks

Celery is integrated for asynchronous processing.

Current implementation:

- Order confirmation task is executed asynchronously after a successful order is created.

Workflow

```
Client
   │
   ▼
Django API
   │
   ▼
Redis Broker
   │
   ▼
Celery Worker
   │
   ▼
Background Task
```

Using Celery ensures that long-running operations do not block API responses.

---

# Design Decisions

Some key design decisions include:

- Business logic separated into a dedicated Service Layer.
- Transaction-safe order creation using `transaction.atomic()`.
- Inventory locking using `select_for_update()` to prevent race conditions.
- Atomic inventory updates using Django `F()` expressions.
- Redis caching to improve API performance.
- Celery for asynchronous task execution.
- Modular Django app architecture.
- Automatic API documentation with drf-spectacular.
- Dockerized environment for consistent development.

---

# Scalability Considerations

The project has been designed with scalability in mind.

- Modular application structure makes future development easier.
- Redis caching reduces database load for frequently requested endpoints.
- Celery allows background task processing without blocking HTTP requests.
- Database transactions guarantee consistency during concurrent order creation.
- Inventory locking prevents overselling in concurrent environments.
- Docker provides reproducible deployment across environments.
- PostgreSQL offers a production-ready relational database backend.
- The architecture can be extended with multiple Celery workers, load balancing, and distributed caching for higher traffic scenarios.

---

# Author

**Nikhil Ambure**

Backend Developer
````

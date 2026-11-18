# IS601 Module 11 — Calculation Model and Validation

This project builds on my Module 10 FastAPI calculator application by adding a SQLAlchemy Calculation model, Pydantic validation schemas, and a factory pattern for handling arithmetic operations. It also includes PostgreSQL integration testing and continues using Docker and GitHub Actions for CI/CD.

## Features

- **FastAPI Calculator:** Supports addition, subtraction, multiplication, and division.
- **SQLAlchemy Models:** Defines User and Calculation models for storing data in PostgreSQL.
- **Pydantic Validation:** Validates calculation inputs, operation types, and division by zero.
- **Factory Pattern:** Selects the appropriate arithmetic operation and creates Calculation objects.
- **User Registration:** Retains secure user registration and Argon2 password hashing from Module 10.
- **Automated Testing:** Includes unit, integration, and end-to-end tests.
- **Docker Compose:** Runs FastAPI, PostgreSQL, and pgAdmin.
- **CI/CD:** Uses GitHub Actions for automated testing, security scanning, and Docker Hub deployment.

## Technologies

Python 3.12, FastAPI, SQLAlchemy, Pydantic, PostgreSQL, pytest, Docker, Docker Compose, GitHub Actions, Playwright, Trivy

## Calculation Model

The SQLAlchemy Calculation model contains the following fields:

| Field | Description |
|---|---|
| id | Unique calculation identifier |
| a | First operand |
| b | Second operand |
| type | Operation type |
| result | Calculated result |

The application supports four operations: `add`, `subtract`, `multiply`, and `divide`.

### Pydantic Schemas

- `CalculationCreate`: Validates incoming operands and operation types.
- `CalculationRead`: Defines how calculation records are serialized.
- `CalculationType`: Restricts operations to the four supported types.

Validation prevents unsupported operations, division by zero, and invalid numeric inputs.

### Factory Pattern

The `CalculationFactory` class uses the existing arithmetic functions to calculate results and create SQLAlchemy Calculation objects.

For example:

```python
data = CalculationCreate(a=10, b=5, type="multiply")
calculation = CalculationFactory.create(data)

print(calculation.result)  # 50.0
```

The factory creates the object, while SQLAlchemy handles database persistence.

Calculation database API endpoints will be implemented in Module 12.

## Running the Application

### Prerequisites

- Git
- Docker and Docker Compose

### Setup

Clone the repository:

```bash
git clone https://github.com/fzheng04/assignment11.git
cd assignment11
```

Build and start the containers:

```bash
docker compose up -d --build
```

The application will be accessible at:

| Service | URL |
|---|---|
| FastAPI Calculator | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |
| pgAdmin | http://localhost:5050 |

Database tables are initialized automatically when the application starts.

Stop the containers:

```bash
docker compose down
```

## Running Tests

Tests can be executed using Docker to ensure the correct PostgreSQL connection and Python environment.

### Unit Tests

```bash
docker compose run --rm web python -m pytest tests/unit/ -v -o addopts=""
```

These tests cover arithmetic operations, factory behavior, Pydantic validation, and existing user functionality.

### PostgreSQL Integration Tests

```bash
docker compose run --rm web python -m pytest tests/integration/ -v -o addopts=""
```

The Module 11 integration tests verify that calculations can be saved to PostgreSQL, retrieved correctly, and validated before insertion.

All six new calculation integration tests passed locally.

### End-to-End Tests

The existing Playwright tests are also included in the project and run through GitHub Actions.

The CI workflow installs the required Playwright browser dependencies before executing them.

## CI/CD Pipeline

GitHub Actions runs automatically on pushes and pull requests to the `main` branch.

The pipeline includes three jobs:

1. **Test:** Runs unit, integration, and end-to-end tests using PostgreSQL.
2. **Security:** Builds the Docker image and scans it using Trivy.
3. **Deploy:** Pushes the Docker image to Docker Hub after the previous jobs succeed.

Python 3.12 is used in both the Dockerfile and GitHub Actions.

During development, Python 3.13 caused a bus error inside Docker. Switching to Python 3.12 resolved the issue and allowed the integration tests to run successfully.

## Docker Hub

Docker Hub Repository:

https://hub.docker.com/r/fzheng04/601_module11

Pull the latest image:

```bash
docker pull fzheng04/601_module11:latest
```

The image requires a PostgreSQL database connection configured through the `DATABASE_URL` environment variable.

## Security

- Passwords are hashed using Argon2.
- Pydantic validates incoming user and calculation data.
- SQLAlchemy manages database interactions without raw SQL.
- User API responses exclude password hashes.
- GitHub Actions secrets store Docker Hub credentials.
- Trivy scans Docker images for known vulnerabilities.

## Project Development

Module 11 builds on the previous FastAPI calculator and secure user registration functionality.

The main additions are the Calculation SQLAlchemy model, Pydantic calculation schemas, factory pattern, and PostgreSQL integration tests.

These changes provide the foundation for implementing calculation database endpoints in Module 12.

## Author

Feiyang Zheng  
NJIT — IS601  
Module 11 Assignment
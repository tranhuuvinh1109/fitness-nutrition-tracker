# GEMINI.md

## Project Overview

This project is a Flask-based REST API for a fitness and nutrition tracker. It provides a comprehensive backend for an application that allows users to track their workouts, meals, water intake, and fitness goals. The API is well-structured, using Flask Blueprints to organize endpoints for different features like user management, food logging, workout tracking, and more. It also includes JWT-based authentication and authorization, and uses SQLAlchemy as an ORM for interacting with a PostgreSQL database. The project is containerized using Docker and Docker Compose, making it easy to set up and run in different environments.

## Building and Running

### Docker

The recommended way to run the application is by using Docker.

1.  **Build the Docker image:**

    ```bash
    docker-compose build
    ```

2.  **Run the application:**

    ```bash
    docker-compose up
    ```

### Local Development

You can also run the application locally without Docker.

1.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

2.  **Activate the virtual environment:**

    *   **Windows:**

        ```bash
        venv\Scripts\activate
        ```

    *   **macOS/Linux:**

        ```bash
        source venv/bin/activate
        ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**

    ```bash
    flask run
    ```

## Testing

The project uses `unittest` for testing. To run the tests, you can use the following command:

```bash
python -m unittest discover tests
```

## Development Conventions

*   **Code Style:** The project uses `flake8` for linting and `black` for code formatting.
*   **API Documentation:** The API is documented using Swagger, which can be accessed at the `/swagger-ui` endpoint.
*   **Database Migrations:** The project uses `Flask-Migrate` to manage database migrations.
*   **Modularity:** The application is organized into blueprints, with each blueprint representing a specific feature. This promotes code reusability and maintainability.
*   **Configuration:** The application uses a `config.py` file to manage different configurations for different environments (development, testing, production).
*   **Containerization:** The application is containerized using Docker, which ensures consistency across different environments.

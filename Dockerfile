FROM python:3.9-slim

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy prodebug directory first to ensure it exists during installation
COPY prodebug ./prodebug/

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Configure Poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies without installing the project itself
RUN poetry install --no-root --only main

# Copy the rest of the application
COPY . .

# Expose the port the app runs on (Cloud Run expects 8080)
EXPOSE 8080

# Command to run the application
CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
FROM python:3.9

WORKDIR /app

# Copy the requirements files and the project to the container
COPY pyproject.toml /app/

# Install Poetry and the project dependencies
RUN pip install poetry && poetry install --no-root

# Copy the entire project to the container
COPY . /app/

# Specify the command to run the application
CMD ["/bin/sh", "-c", "poetry update && poetry run gunicorn reservations.wsgi"]

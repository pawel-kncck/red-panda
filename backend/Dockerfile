FROM python:3.13.7-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml /app/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

ENV PYTHONPATH=/app

# Copy scripts
COPY ./scripts /app/scripts
RUN chmod +x /app/scripts/*.sh

# Copy alembic configuration
COPY ./alembic.ini /app/

# Copy application code
COPY ./app /app/app
COPY ./alembic /app/alembic

CMD ["fastapi", "run", "--workers", "4", "app/main.py"]
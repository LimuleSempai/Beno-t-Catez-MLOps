# Use the official Python image
FROM python:3.11.6-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy poetry files
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application
COPY . /app/

# Expose the port
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app.py"]

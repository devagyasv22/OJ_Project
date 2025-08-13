FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=OJ.settings
ENV PYTHONUNBUFFERED=1

# Run migrations
RUN python manage.py migrate --noinput

# Expose port
EXPOSE 8000

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

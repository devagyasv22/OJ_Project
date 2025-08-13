FROM python:3.9

WORKDIR /app

# Copy only requirements first
COPY requirements.txt .

# Install dependencies inside container
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Environment variables
ENV DJANGO_SETTINGS_MODULE=OJ.settings
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Migrate and start server at container start
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]

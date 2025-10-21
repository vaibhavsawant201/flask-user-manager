# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose Flask port
EXPOSE 5000

# Run the app with gunicorn (for production use)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

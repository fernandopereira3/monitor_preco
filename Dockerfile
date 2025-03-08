FROM selenium/standalone-chrome

# Set working directory
WORKDIR /app

# Copy application files
COPY requirements.txt .
COPY . .

# Install dependencies
RUN apt-get update && apt-get install -y \
    source ./bin/activate \
    pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Run the application
CMD ["python", "executar_monitoramento.py"]
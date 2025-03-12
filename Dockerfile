FROM ubuntu:latest

# Set working directory
WORKDIR /app

# Copy application files
COPY requirements.txt .
COPY . .



# Run the application
CMD ["python", "executar_monitoramento.py"]
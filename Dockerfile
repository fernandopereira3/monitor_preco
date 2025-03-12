FROM selenium/standalone-chrome

# Set working directory
WORKDIR /app

# Copy application files
COPY requirements.txt .
COPY . .

# Install dependencies
RUN cd /app
RUN sudo python3 -m venv .
RUN source ./bin/activate
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Run the application
CMD ["python", "executar_monitoramento.py"]
FROM fedora:latest

# Set working directory
WORKDIR /app

# Copy application files
COPY . .
RUN dnf update  -y
RUN dnf install python313 -y
RUN dnf install fedora-workstation-repositories -y \
    && dnf config-manager setopt google-chrome.enabled=1 -y \
    && dnf install google-chrome-stable -y
    
RUN cd /app 
RUN source ./bin/activate 
RUN pip install -r requirements.txt

# Run the application
CMD ["python", "executar_monitoramento.py"]
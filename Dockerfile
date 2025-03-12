FROM fedora:latest

# Set working directory
WORKDIR /app

# Copy application files
COPY . .
RUN dnf update  -y
RUN dnf install python313 -y
RUN dnf install fedora-workstation-repositories -y
RUN dnf config-manager setopt google-chrome.enabled=1 -y
RUN dnf install google-chrome-stable -y
RUN cd /app 
RUN source ./bin/activate 
RUN pip install -r requirements.txt

# Run the application
CMD ["python3", "executar_monitoramento.py"]
FROM fedora:latest

# Set working directory
WORKDIR /app

# Copy application files
COPY . .
RUN dnf update  -y
RUN dnf install python313 -y
RUN dnf install python3-pip -y
RUN dnf install fedora-workstation-repositories -y
RUN dnf config-manager setopt google-chrome.enabled=1 -y
RUN dnf install google-chrome-stable -y
RUN cd /app 
RUN python3 -m venv .
RUN python3 -m pip install -r requirements.txt

# Run the application
CMD ["python3", "executar_monitoramento.py"]

# Declaring /app as a volume is correct if you want to share or persist data outside the container.
# Keep in mind that any files added in previous layers (e.g., via COPY) will be hidden when an external volume is mounted here.
VOLUME ["/app/data"]

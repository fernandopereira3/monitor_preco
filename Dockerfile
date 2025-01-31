# Use the Ubuntu 22.04 base image
FROM ubuntu:22.04
# Add Python 3.8 to the image
FROM python:3.13
# Update package lists for the Ubuntu system
RUN apt -y update
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb
# Install the 'unzip' package
RUN apt install unzip
# Download ChromeDriver binary version 114.0.5735.90 for Linux
RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
# Unzip the downloaded ChromeDriver binary
RUN unzip chromedriver_linux64.zip
# Move the ChromeDriver binary to /usr/bin
RUN mv chromedriver /usr/bin/chromedriver
# Print the version of Google Chrome installed
RUN google-chrome --version
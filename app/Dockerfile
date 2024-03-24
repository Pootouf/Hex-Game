FROM node:21.7.0-slim

# Python installation
RUN apt update -y \
    && apt install python3 python3-pip python3-flask python3-gi -y

# Define workdir
WORKDIR /app

# NPM Configuration
RUN npm install -g npm

# Get npm config
COPY ./package.json ./package-lock.json /app/

# Tailwind installation
RUN npm install && npm install tailwindcss@3.4.1

# Copy project files
COPY . /app

EXPOSE 5000
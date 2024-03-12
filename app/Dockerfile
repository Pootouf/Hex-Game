FROM node:21.7.0-slim

# Python installation
RUN apt update -y \
    && apt install python3 python3-pip -y

# Define workdir
WORKDIR /app

# NPM Configuration
RUN npm install -g npm

# Get npm config
COPY ./package.json /app

RUN npm install

# Flask installation
RUN apt install python3-flask -y

# Copy project files
COPY . /app

EXPOSE 5000
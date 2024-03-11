FROM node:21.7.0-slim
RUN apt update -y \
    && apt install python3 python3-pip -y \
RUN pip install pyscript
WORKDIR /app
COPY . /app
EXPOSE 8000
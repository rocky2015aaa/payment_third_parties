# Base Image
FROM python:3.8.1-slim-buster

# Variables for dockerfile.
ENV WORKDIR=/usr/src/app
ENV USER=app
ENV APP_HOME=/home/app/web
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# Setting workdir for variables.
WORKDIR $WORKDIR

# Python specfic command execution.
RUN pip install --upgrade pip
COPY ./requirements.txt $WORKDIR/requirements.txt
RUN pip install -r requirements.txt

# Application Layer Permissions
RUN adduser --system --group $USER
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Copy Application to container
COPY . $APP_HOME
RUN chown -R $USER:$USER $APP_HOME
USER $USER

# Server start command.
# CMD uvicorn app.main:app --host 0.0.0.0 --port 8000

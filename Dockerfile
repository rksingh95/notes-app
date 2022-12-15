# base image
FROM python:3.10-alpine
# install dependencies
RUN python3 -m pip install --upgrade pip
# set environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH="/home/user/.local/bin:${PATH}"
# working directory
WORKDIR /code
# copy whole project to your docker home directory.
COPY . /code
RUN adduser -D user && chown -R user:user /code
USER user

COPY ./requirements.txt /requirements.txt
# run this command to install all dependencies
RUN pip install --no-cache-dir -r /requirements.txt

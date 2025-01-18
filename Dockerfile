# FROM python:3.8-slim-buster
# Python Based Docker
FROM python:latest

# Installing Packages
RUN apt update && apt upgrade -y
RUN apt install git curl python3-pip ffmpeg -y

# Updating Pip Packages
RUN pip3 install -U pip

# Copying Requirements
COPY requirements.txt /requirements.txt

# Installing Requirements
RUN cd /
RUN pip3 install -U -r requirements.txt
RUN mkdir /autodelete
WORKDIR /autodelete

# Running MessageSearchBot
# CMD ["python", "bot.py"]

# COPY . .
# RUN pip3 install -r requirements.txt

CMD ["python3","bot.py"]

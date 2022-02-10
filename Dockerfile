FROM python:3.7-slim-buster

RUN apt-get update

RUN mkdir -p /src/fb_group

COPY requirements.txt /src/

RUN pip install -r /src/requirements.txt

COPY ./src/fb_group/ /src/fb_group/

WORKDIR /src

ENTRYPOINT ["python", "-m", "fb_group.run"]
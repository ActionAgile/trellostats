FROM python:2
RUN apt-get update -qq && apt-get install -y python-pip python-dev build-essential
RUN pip install trellostats
ENTRYPOINT trellostats runapiserver 0.0.0.0 8081

FROM python:2
ADD . /code
WORKDIR /code
CMD ["pip install trellostats]
EXEC trellostats runapiserver 0.0.0.0 80

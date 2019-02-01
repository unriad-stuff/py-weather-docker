FROM python
MAINTAINER Andrew Chumchal <andrew@andrewchumchal.com>

VOLUME /src/
COPY saver.py generate_points.py requirements.txt /src/
COPY config.ini /src/config.example.ini
ADD py-weather /src/py-weather
WORKDIR /src

RUN pip install -r requirements.txt
RUN python generate_points.py

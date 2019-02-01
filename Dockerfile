FROM python
MAINTAINER Andrew Chumchal <andrew@andrewchumchal.com>

VOLUME /src
COPY . /src/py-weather
COPY saver.py generate_points.py requirements.txt python_runner.py /src/
COPY config.ini /src/config.example.ini
WORKDIR /src

RUN pip install -r requirements.txt
CMD ["python3", "-u", "/src/generate_points.py"]
CMD ["python3", "-u", "/src/python_runner.py"]

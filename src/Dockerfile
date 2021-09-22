FROM python:3.9

ENV workdir=/usr/src/app
WORKDIR $workdir

RUN apt-get update
RUN apt install -y libzbar0 libzbar-dev nano
RUN pip install zbarlight PyYAML==5.4.1 flask

COPY server.py server.py
COPY decode_utils.py decode_utils.py

CMD [ "python", "server.py" ]

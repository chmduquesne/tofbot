FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python2 virtualenv

COPY . /opt

WORKDIR /opt

RUN virtualenv -p python2 venv

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt

ENV TOFBOT_NICK=tofbot
ENV TOFBOT_DEBUG=true
ENV TOFBOT_CHAN=#soulakins
CMD ["python", "bot.py"]

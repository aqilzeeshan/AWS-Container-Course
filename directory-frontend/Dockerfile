FROM python:3.9-slim-buster

# needed to capture stderr output
# https://github.com/bottlepy/bottle/issues/1130#issuecomment-478096704
# https://stackoverflow.com/a/59812588/109102
ENV PYTHONUNBUFFERED=1 

COPY app /app

WORKDIR /app

RUN pip3 install -r requirements.txt && \
    apt update  && \
    apt install -y procps curl dnsutils

EXPOSE 80

ENV FLASK_APP=application.py

CMD flask run --host 0.0.0.0 --port 80

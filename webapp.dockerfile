FROM python:3.9.12
LABEL maintainer="Jiahao Zhang <jiahao.zhang@anu.edu.au>"

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
RUN pip install --no-cache-dir gunicorn
RUN rm /requirements.txt

RUN mkdir -p /influencemap
COPY webapp /influencemap/webapp/
COPY core /influencemap/core/
COPY graph /influencemap/graph/

WORKDIR /influencemap/
ENV KONIGSBERG_URL="url_to_konigsberg"
ENV ELASTICSEARCH_URL="url_to_elasticsearch"
ENV GUNICORN_CMD_ARGS="--workers 32 --timeout 90 --graceful-timeout 90 --bind 0.0.0.0:8001"
ENTRYPOINT gunicorn $GUNICORN_CMD_ARGS webapp:flask_app

FROM alpine:3.8

ENV GUNICORN_WORKER_AMOUNT 4
ENV GUNICORN_TIMEOUT 300
ENV GUNICORN_RELOAD ""

RUN apk add python3 python3-dev gcc libc-dev && rm -rf /var/cache/apk/*

RUN pip3 install flask requests nltk conllu gunicorn

RUN python3 -c "import nltk; nltk.download('punkt', '/usr/share/nltk_data')"

WORKDIR /app

COPY src ./

ENV CONF_FILE=/app/conf/config.ini 
COPY conf/config.ini $CONF_FILE

COPY language-resources ./language-resources/

RUN chgrp -R 0 /app \
    && chmod -R g+rwX /app

EXPOSE 5000

USER 9008

COPY run /run.sh

ENTRYPOINT [ "/run.sh" ]

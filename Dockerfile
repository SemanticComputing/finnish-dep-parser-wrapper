FROM alpine:3.8

ENV GUNICORN_WORKER_AMOUNT 4
ENV GUNICORN_TIMEOUT 300
ENV GUNICORN_RELOAD ""

RUN apk add python3 python3-dev gcc libc-dev && rm -rf /var/cache/apk/*

RUN pip3 install flask requests nltk conllu gunicorn

RUN python3 -c "import nltk; nltk.download('punkt', '/usr/share/nltk_data')"

WORKDIR /app

COPY src ./

ENV FDP_CONFIG_ENV DEFAULT
ENV CONF_FILE=/app/conf/config.ini 
COPY conf/config.ini $CONF_FILE

ENV LOG_CONF_FILE=/app/conf/logging.ini
COPY conf/logging.ini $LOG_CONF_FILE
RUN sed -i s/logging\.handlers\.RotatingFileHandler/logging\.StreamHandler/ $LOG_CONF_FILE \
 && sed -i s/logging\.FileHandler/logging\.StreamHandler/ $LOG_CONF_FILE \
 && sed -E -i s/^args=.+$/args=\(sys.stdout,\)/ $LOG_CONF_FILE

COPY language-resources ./language-resources/

RUN chgrp -R 0 /app \
    && chmod -R g+rwX /app

EXPOSE 5000

USER 9008

COPY run /run.sh

ENTRYPOINT [ "/run.sh" ]

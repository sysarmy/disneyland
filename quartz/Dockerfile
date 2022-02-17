FROM python:3.7

WORKDIR /app
COPY ./quartz.py .
COPY ./run-quartz.sh .

RUN chmod +x /app/run-quartz.sh

RUN apt-get update && \
    apt-get -y install cron && \
    rm -rf /var/lib/apt/lists/*

RUN pip install icmplib requests && \
    pip cache purge

RUN echo "*/5 * * * * root /app/run-quartz.sh" > /etc/cron.d/qartz

RUN mkdir /root/.config

ENV EXECUTION_ENV=DOCKER

CMD ["/app/run-quartz.sh"]
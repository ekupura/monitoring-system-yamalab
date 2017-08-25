FROM ubuntu:latest
RUN apt update
RUN apt install -y cron python3 python3-pip
RUN pip3 install influxdb psutil
COPY simple-cron /etc/cron.d/simple-cron
RUN chmod 0644 /etc/cron.d/simple-cron
COPY ./send-metrics.py /
COPY ./script.sh /
RUN chmod +x /script.sh
RUN chmod 0644 /etc/cron.d/simple-cron
CMD cron && touch /etc/cron.d/simple-cron && tail -f /dev/null


FROM nvidia/cuda:8.0-runtime
RUN apt update
RUN apt install -y python3 python3-pip
RUN pip3 install influxdb psutil
COPY ./send.py /
COPY ./nvidia.py /
CMD python3 send.py


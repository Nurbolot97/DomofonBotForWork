#TELEGRAM BOT FOR COURIERS WORKING PROCESS

FROM python:3.8-alpine
MAINTAINER Daiyrkanov Nurbolot "ndaiyrkanov@gmail.com"
WORKDIR /AddressBot
ADD . /AddressBot
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "start.py"]

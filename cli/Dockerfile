FROM python:3.11

RUN apt update && apt install jq -y

COPY . /root/insight
WORKDIR /root/insight
RUN pip install .

WORKDIR /root
RUN rm -rf /root/insight
RUN mkdir /root/.config

CMD /bin/bash

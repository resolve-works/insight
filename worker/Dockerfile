FROM python

COPY . /home
WORKDIR /home
RUN pip install .

CMD insight-worker process-messages

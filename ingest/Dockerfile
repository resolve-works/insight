FROM python

RUN apt update && apt install -y ocrmypdf tesseract-ocr-nld

COPY . /home
WORKDIR /home
RUN pip install .

CMD insight-ingest process-messages

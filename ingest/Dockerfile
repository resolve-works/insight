FROM python

RUN apt update && apt install -y tesseract-ocr tesseract-ocr-nld ghostscript

COPY . /home
WORKDIR /home
RUN pip install .

CMD insight-ingest process-messages

FROM jbarlow83/ocrmypdf-alpine:latest

RUN apk add tesseract-ocr-data-nld

COPY . /home/insight
WORKDIR /home/insight
RUN pip install .
RUN rm -rf /home/insight

ENV NLTK_DATA=/tmp/llama_index
RUN python3 -c 'import nltk; import os; nltk.download("punkt", download_dir=os.environ.get("NLTK_DATA"));'

WORKDIR /home
CMD insight-worker process-messages

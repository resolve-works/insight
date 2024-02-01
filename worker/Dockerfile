FROM jbarlow83/ocrmypdf-alpine:latest

RUN apk add bash ca-certificates tesseract-ocr-data-nld mupdf-dev build-base linux-headers python3-dev

COPY . /home/insight
WORKDIR /home/insight
RUN pip install .
RUN rm -rf /home/insight

ENV NLTK_DATA=/tmp/llama_index
RUN python3 -c 'import nltk; import os; nltk.download("punkt", download_dir=os.environ.get("NLTK_DATA"));'

WORKDIR /home
ENTRYPOINT /app/.venv/bin/insight-worker
CMD process-messages

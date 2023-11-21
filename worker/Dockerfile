FROM python:3.11

RUN apt update && apt install -y tesseract-ocr tesseract-ocr-nld ghostscript libleptonica-dev pngquant

RUN git clone https://github.com/agl/jbig2enc /home/jbig2enc
WORKDIR /home/jbig2enc
RUN ./autogen.sh
RUN ./configure && make
RUN make install
RUN rm -rf /home/jbig2enc

COPY . /home/insight
WORKDIR /home/insight
RUN pip install .
RUN rm -rf /home/insight

ENV NLTK_DATA=/tmp/llama_index
RUN python3 -c 'import nltk; import os; nltk.download("punkt", download_dir=os.environ.get("NLTK_DATA"));'

WORKDIR /home
CMD insight-worker process-messages

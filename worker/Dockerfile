FROM python

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

WORKDIR /home
CMD insight-worker process-messages

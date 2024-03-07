FROM python:3.11

# Install latest ghostscript to fix a regression that breaks OCRmyPDF
WORKDIR /home
RUN wget https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10021/ghostscript-10.02.1.tar.gz
RUN tar xfz ghostscript-10.02.1.tar.gz
WORKDIR /home/ghostscript-10.02.1
RUN ./configure && make
RUN make install
RUN rm -rf /home/ghostscript-10.02.1

RUN apt update && apt install -y tesseract-ocr tesseract-ocr-nld libleptonica-dev pngquant

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


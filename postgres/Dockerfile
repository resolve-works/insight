FROM postgres:15

RUN apt update && apt install -y postgresql-15-pgvector postgresql-plpython3-15 python3.11 python3-pip
WORKDIR /home
COPY requirements.txt .
RUN pip install --break-system-packages -r requirements.txt
RUN rm requirements.txt

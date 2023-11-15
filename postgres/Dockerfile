FROM postgres:15

RUN apt update && apt install -y postgresql-15-pgvector postgresql-plpython3-15 python3.11 python3-pip
RUN pip install --break-system-packages asyncio asyncpg llama-index pgvector psycopg2-binary sqlalchemy minio

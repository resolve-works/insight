from sqlalchemy import Column, DateTime, Double, Enum, Integer, MetaData, Table, Text, Uuid

metadata = MetaData()


t_documents = Table(
    'documents', metadata,
    Column('id', Uuid),
    Column('owner_id', Uuid),
    Column('file_id', Uuid),
    Column('path', Text),
    Column('from_page', Integer),
    Column('to_page', Integer),
    Column('name', Text),
    Column('status', Enum('ingesting', 'idle', name='document_status')),
    schema='public'
)


t_files = Table(
    'files', metadata,
    Column('id', Uuid),
    Column('owner_id', Uuid),
    Column('name', Text),
    Column('path', Text),
    Column('pages', Integer),
    Column('status', Enum('uploading', 'analyzing', 'idle', name='file_status')),
    Column('created_at', DateTime(True)),
    Column('updated_at', DateTime(True)),
    schema='public'
)


t_prompts = Table(
    'prompts', metadata,
    Column('id', Uuid),
    Column('owner_id', Uuid),
    Column('query', Text),
    Column('similarity_top_k', Integer),
    Column('response', Text),
    Column('status', Enum('answering', 'idle', name='prompt_status')),
    Column('created_at', DateTime(True)),
    Column('updated_at', DateTime(True)),
    schema='public'
)


t_sources = Table(
    'sources', metadata,
    Column('prompt_id', Uuid),
    Column('file_id', Uuid),
    Column('index', Integer),
    Column('score', Double(53)),
    schema='public'
)

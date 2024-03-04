from typing import Any, List, Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import BigInteger, DateTime, Double, Enum, ForeignKeyConstraint, Integer, JSON, PrimaryKeyConstraint, String, Text, Uuid, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import uuid

class Base(DeclarativeBase):
    pass


class DataPage(Base):
    __tablename__ = 'data_page'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='data_page_pkey'),
        {'schema': 'private'}
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    text_: Mapped[str] = mapped_column('text', String)
    metadata_: Mapped[Optional[dict]] = mapped_column(JSON)
    node_id: Mapped[Optional[str]] = mapped_column(String)
    embedding: Mapped[Optional[Any]] = mapped_column(Vector(1536))


class Files(Base):
    __tablename__ = 'files'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='files_pkey'),
        {'schema': 'private'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    owner_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    path: Mapped[str] = mapped_column(Text)
    name: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Enum('uploading', 'analyzing', 'idle', name='file_status'), server_default=text("'uploading'::file_status"))
    pages: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    documents: Mapped[List['Documents']] = relationship('Documents', back_populates='file')
    sources: Mapped[List['Sources']] = relationship('Sources', back_populates='file')


class Prompts(Base):
    __tablename__ = 'prompts'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='prompts_pkey'),
        {'schema': 'private'}
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    query: Mapped[str] = mapped_column(Text)
    similarity_top_k: Mapped[int] = mapped_column(Integer, server_default=text('3'))
    status: Mapped[str] = mapped_column(Enum('answering', 'idle', name='prompt_status'), server_default=text("'answering'::prompt_status"))
    response: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    sources: Mapped[List['Sources']] = relationship('Sources', back_populates='prompt')


class Documents(Base):
    __tablename__ = 'documents'
    __table_args__ = (
        ForeignKeyConstraint(['file_id'], ['private.files.id'], ondelete='CASCADE', name='documents_file_id_fkey'),
        PrimaryKeyConstraint('id', name='documents_pkey'),
        {'schema': 'private'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    file_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    path: Mapped[str] = mapped_column(Text)
    from_page: Mapped[int] = mapped_column(Integer)
    to_page: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(Enum('ingesting', 'idle', name='document_status'), server_default=text("'ingesting'::document_status"))
    name: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    file: Mapped['Files'] = relationship('Files', back_populates='documents')


class Sources(Base):
    __tablename__ = 'sources'
    __table_args__ = (
        ForeignKeyConstraint(['file_id'], ['private.files.id'], ondelete='CASCADE', name='sources_file_id_fkey'),
        ForeignKeyConstraint(['prompt_id'], ['private.prompts.id'], ondelete='CASCADE', name='sources_prompt_id_fkey'),
        PrimaryKeyConstraint('id', name='sources_pkey'),
        {'schema': 'private'}
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    prompt_id: Mapped[int] = mapped_column(BigInteger)
    file_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    index: Mapped[int] = mapped_column(Integer)
    score: Mapped[float] = mapped_column(Double(53))

    file: Mapped['Files'] = relationship('Files', back_populates='sources')
    prompt: Mapped['Prompts'] = relationship('Prompts', back_populates='sources')

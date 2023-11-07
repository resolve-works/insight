from typing import List

from sqlalchemy import ForeignKeyConstraint, PrimaryKeyConstraint, Text, Uuid, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import uuid

class Base(DeclarativeBase):
    pass


class Pagestreams(Base):
    __tablename__ = 'pagestreams'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pagestreams_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    path: Mapped[str] = mapped_column(Text)
    name: Mapped[str] = mapped_column(Text)

    files: Mapped[List['Files']] = relationship('Files', back_populates='pagestream')


class Files(Base):
    __tablename__ = 'files'
    __table_args__ = (
        ForeignKeyConstraint(['pagestream_id'], ['pagestreams.id'], ondelete='RESTRICT', name='files_pagestream_id_fkey'),
        PrimaryKeyConstraint('id', name='files_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    pagestream_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    name: Mapped[str] = mapped_column(Text)

    pagestream: Mapped['Pagestreams'] = relationship('Pagestreams', back_populates='files')

from typing import List, Optional

from sqlalchemy import ForeignKeyConstraint, Integer, PrimaryKeyConstraint, Text, Uuid, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import uuid

class Base(DeclarativeBase):
    pass


class Pagestream(Base):
    __tablename__ = 'pagestream'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pagestream_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    path: Mapped[str] = mapped_column(Text)
    name: Mapped[str] = mapped_column(Text)

    file: Mapped[List['File']] = relationship('File', back_populates='pagestream')
    page: Mapped[List['Page']] = relationship('Page', back_populates='pagestream')


class File(Base):
    __tablename__ = 'file'
    __table_args__ = (
        ForeignKeyConstraint(['pagestream_id'], ['pagestream.id'], ondelete='RESTRICT', name='file_pagestream_id_fkey'),
        PrimaryKeyConstraint('id', name='file_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    pagestream_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    from_page: Mapped[int] = mapped_column(Integer)
    to_page: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)

    pagestream: Mapped['Pagestream'] = relationship('Pagestream', back_populates='file')


class Page(Base):
    __tablename__ = 'page'
    __table_args__ = (
        ForeignKeyConstraint(['pagestream_id'], ['pagestream.id'], ondelete='RESTRICT', name='page_pagestream_id_fkey'),
        PrimaryKeyConstraint('id', name='page_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    pagestream_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    index: Mapped[int] = mapped_column(Integer)
    contents: Mapped[Optional[str]] = mapped_column(Text)

    pagestream: Mapped['Pagestream'] = relationship('Pagestream', back_populates='page')

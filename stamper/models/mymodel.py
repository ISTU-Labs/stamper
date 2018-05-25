from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    nick = Column(Text)
    name = Column(Text)
    passwd = Column(Text)  # Hash
    email = Column(Text)

    images = relationship("Image", back_populates="user")

    isvalid = True


class Mark(Base):
    __tablename__ = 'mark'

    value = Column(Text)

    image_id = Column(Integer, ForeignKey('image.id'), primary_key=True),
    tag_id = Column(Integer, ForeignKey('tag.id'), primary_key=True)

    # tag = relationship("Tag", back_populates="images")
    # image = relationship("Image", back_populates="tags")


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    mmhash = Column(Text)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, back_populates="images")

    # tags = relationship(Mark, back_populates="image")


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(Text)

    # images = relationship(Mark, back_populates="tag")


Index('user_nick_index', User.nick, unique=True, mysql_length=255)
Index('user_name_index', User.name, unique=False, mysql_length=255)

Index('image_mmhash_index', Image.mmhash, unique=True, mysql_length=255)
Index('tage_name_index', Tag.name, unique=False, mysql_length=255)

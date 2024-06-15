from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import String, ForeignKey, Text, Integer, Table, Column, MetaData, TIMESTAMP, func
from check_rights import CheckRights
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask import url_for
from datetime import datetime
import os

# Базовый класс для всех моделей
class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

db = SQLAlchemy(model_class=Base)

ADMIN_ROLE_ID=1
MODERATOR_ROLE_ID=2
USER_ROLE_ID=3

class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

class User(Base, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), nullable=False)

    role = relationship("Role")

    def is_admin(self): 
        return ADMIN_ROLE_ID == self.role_id
    
    def is_moderator(self): 
        return MODERATOR_ROLE_ID == self.role_id
    
    def is_user(self): 
        return USER_ROLE_ID == self.role_id

    def can(self, action, record=None):
        check_rights = CheckRights(record)
        method = getattr(check_rights, action, None)
        if method:
            return method()
        return False

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return ' '.join([self.last_name, self.first_name, self.middle_name or ''])

    def __repr__(self):
        return '<User %r>' % self.username

class Genre(Base):
    __tablename__ = 'genres'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

class Cover(Base):
    __tablename__ = 'covers'

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    md5_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f'<Image {self.filename}>'

    @property
    def storage_filename(self):
        _, ext = os.path.splitext(self.filename)
        return f"{self.md5_hash}{ext}" 

    @property
    def url(self):
        return url_for('image', image_id=self.id, _external=True)

book_genre_table = Table('book_genre', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)

class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    publisher: Mapped[str] = mapped_column(String(100), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    pages: Mapped[int] = mapped_column(Integer, nullable=False)
    cover_id: Mapped[int] = mapped_column(Integer, ForeignKey('covers.id'), nullable=False)

    cover = relationship("Cover", single_parent=True, cascade="all, delete, delete-orphan")
    genres = relationship("Genre", secondary=book_genre_table, back_populates="books")
    comments = relationship("Comment", back_populates="book", cascade="all, delete-orphan")

Genre.books = relationship("Book", secondary=book_genre_table, back_populates="genres")


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    date_added: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)

    book = relationship("Book", back_populates="comments")
    user = relationship("User")
    

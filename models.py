import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import select
from datetime import datetime

Base = declarative_base()

class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    books = relationship("Book", secondary="book_author", back_populates="authors")


class BookAuthor(Base):
    __tablename__ = 'book_author'

    book_id = Column(Integer, ForeignKey('book.id'), primary_key=True)
    author_id = Column(Integer, ForeignKey('author.id'), primary_key=True)


class Publisher(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    books = relationship("Book", back_populates="publisher")

class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    publisher_id = Column(Integer, ForeignKey('publisher.id'), nullable=False)
    publisher = relationship("Publisher", back_populates="books")
    stocks = relationship("Stock", back_populates="book")
    authors = relationship("Author", secondary="book_author", back_populates="books")
    
class Shop(Base):
    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    stocks = relationship("Stock", back_populates="shop")


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    shop_id = Column(Integer, ForeignKey('shop.id'), nullable=False)
    count = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    sale = relationship("Sale", back_populates="stock")
    book = relationship("Book", back_populates="stocks")
    shop = relationship("Shop", back_populates="stocks")


class Sale(Base):
    __tablename__ = 'sale'

    id = Column(Integer, primary_key=True)
    stock_id = Column(Integer, ForeignKey('stock.id'), nullable=False)
    date_sale = Column(Date, nullable=False)
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
    stock = relationship("Stock", back_populates="sale")


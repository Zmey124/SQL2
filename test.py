import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import select
from datetime import datetime
from models import Author, BookAuthor, Publisher, Book, Shop, Stock, Sale


Base = declarative_base()


def create_database():
    engine = create_engine("postgresql://postgres:1234@localhost:5432/test_netology")
    
    
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return engine


def fill_database(engine):
    
    Session = sessionmaker(bind=engine)
    session = Session()

    
    try:
        
        author1 = session.query(Author).filter(Author.name == "Пушкин").first()
        if not author1:
            author1 = Author(name="Пушкин")
            session.add(author1)
            
        author2 = session.query(Author).filter(Author.name == "Лермонтов").first()
        if not author2:
            author2 = Author(name="Лермонтов")
            session.add(author2)

        session.commit()

        
        publisher1 = session.query(Publisher).filter(Publisher.name == "Издательство 1").first()
        if not publisher1:
            publisher1 = Publisher(name="Издательство 1")
            session.add(publisher1)
        
        publisher2 = session.query(Publisher).filter(Publisher.name == "Издательство 2").first()
        if not publisher2:
            publisher2 = Publisher(name="Издательство 2")
            session.add(publisher2)

        publisher3 = session.query(Publisher).filter(Publisher.name == "Издательство 3").first()
        if not publisher3:
            publisher3 = Publisher(name="Издательство 3")
            session.add(publisher3)

        session.commit()
        
       
        book1 = session.query(Book).filter(Book.title == "Капитанская дочка").first()
        if not book1:
            book1 = Book(title="Капитанская дочка", publisher_id=publisher1.id)
            book1.authors.append(author1)
            session.add(book1)
        book2 = session.query(Book).filter(Book.title == "Руслан и Людмила").first()
        if not book2:
            book2 = Book(title="Руслан и Людмила", publisher_id=publisher1.id)
            book2.authors.append(author1)
            session.add(book2)

        book3 = session.query(Book).filter(Book.title == "Евгений Онегин").first()
        if not book3:
             book3 = Book(title="Евгений Онегин", publisher_id=publisher2.id)
             book3.authors.append(author1)
             session.add(book3)
        
        book4 = session.query(Book).filter(Book.title == "Герой нашего времени").first()
        if not book4:
            book4 = Book(title="Герой нашего времени", publisher_id=publisher3.id)
            book4.authors.append(author2)
            session.add(book4)
        session.commit()


        shop1 = session.query(Shop).filter(Shop.name == "Буквоед").first()
        if not shop1:
            shop1 = Shop(name="Буквоед")
            session.add(shop1)
        shop2 = session.query(Shop).filter(Shop.name == "Лабиринт").first()
        if not shop2:
            shop2 = Shop(name="Лабиринт")
            session.add(shop2)
        shop3 = session.query(Shop).filter(Shop.name == "Книжный дом").first()
        if not shop3:
           shop3 = Shop(name="Книжный дом")
           session.add(shop3)
        session.commit()

        stock1 = session.query(Stock).filter(Stock.book_id == book1.id, Stock.shop_id == shop1.id).first()
        if not stock1:
            stock1 = Stock(book_id=book1.id, shop_id=shop1.id, count=10, price=600.0)
            session.add(stock1)
        stock2 = session.query(Stock).filter(Stock.book_id == book2.id, Stock.shop_id == shop1.id).first()
        if not stock2:
            stock2 = Stock(book_id=book2.id, shop_id=shop1.id, count=5, price=500.0)
            session.add(stock2)
        stock3 = session.query(Stock).filter(Stock.book_id == book1.id, Stock.shop_id == shop2.id).first()
        if not stock3:
            stock3 = Stock(book_id=book1.id, shop_id=shop2.id, count=5, price=580.0)
            session.add(stock3)
        stock4 = session.query(Stock).filter(Stock.book_id == book3.id, Stock.shop_id == shop3.id).first()
        if not stock4:
            stock4 = Stock(book_id=book3.id, shop_id=shop3.id, count=5, price=490.0)
            session.add(stock4)

        session.commit()


        sale1 = Sale(stock_id=stock1.id, date_sale=datetime.strptime("2022-11-09", "%Y-%m-%d").date(), price=600.0, count=1)
        sale2 = Sale(stock_id=stock2.id, date_sale=datetime.strptime("2022-11-08", "%Y-%m-%d").date(), price=500.0, count=1)
        sale3 = Sale(stock_id=stock3.id, date_sale=datetime.strptime("2022-11-05", "%Y-%m-%d").date(), price=580.0, count=1)
        sale4 = Sale(stock_id=stock4.id, date_sale=datetime.strptime("2022-11-02", "%Y-%m-%d").date(), price=490.0, count=1)
        sale5 = Sale(stock_id=stock1.id, date_sale=datetime.strptime("2022-10-26", "%Y-%m-%d").date(), price=600.0, count=1)
        session.add_all([sale1, sale2, sale3, sale4, sale5])
        session.commit()
        
    except Exception as e:
        session.rollback()
        print(f"Ошибка при заполнении БД: {e}")
    finally:
         session.close()



def get_sales_by_author(engine, author_name):
    Session = sessionmaker(bind=engine)
    session = Session()

    author_query = session.query(Author).filter(Author.name == author_name).first()

    if not author_query:
        print(f"Автор с именем '{author_name}' не найден.")
        return

    sales_query = session.query(
            Book.title,
            Shop.name,
            Sale.price,
            Sale.date_sale
        ).join(
            BookAuthor, Book.id == BookAuthor.book_id
        ).join(
             Author, BookAuthor.author_id == Author.id
        ).join(
            Stock, Book.id == Stock.book_id
        ).join(
            Shop, Stock.shop_id == Shop.id
        ).join(
            Sale, Stock.id == Sale.stock_id
        ).filter(
            Author.id == author_query.id
        ).all()
        

    if not sales_query:
        print(f"Нет данных о продажах книг автора '{author_name}'.")
        return

    for book_title, shop_name, sale_price, sale_date in sales_query:
        print(f"{book_title} | {shop_name} | {sale_price} | {sale_date.strftime('%d-%m-%Y')}")

    session.close()



if __name__ == "__main__":
    engine = create_database()
    fill_database(engine)

    author_name = input("Введите имя автора: ")

    get_sales_by_author(engine, author_name)
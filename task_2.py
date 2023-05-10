import os
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from task_1 import Publisher, Shop, Book, Stock, Sale

login = os.getenv('login')
password = os.getenv('password')
adress = os.getenv('adress')
db_name = os.getenv('db_name')

DSN = f'postgresql://{login}:{password}@{adress}/{db_name}'
engine = sq.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

def get_sales(engine):
    input_str = input('Введите id или имя издателя:\n')

    with Session() as session:
        query =session.query(
        Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale
        ).join(Publisher).join(Stock).join(Shop).join(Sale)
        
    if input_str.isdigit():
        publisher_id = int(input_str)
        query = query.filter(Publisher.id == publisher_id)
    else:
        publisher_name = input_str
        query = query.filter(Publisher.name == publisher_name)

    query_result = query.all()
    
    max_len_book = Book.title.type.length
    max_len_shop = Shop.name.type.length
    max_len_amt = 10

    for book, shop, price, count, date in query_result:
        purchase_str = str((price * count))
        date_str = str(date)[:19]
        print(f'{book.ljust(max_len_book).strip()} | {shop.ljust(max_len_shop).strip()} | {purchase_str.ljust(max_len_amt).strip()} y.e. | {date_str.strip()}')

if __name__ == '__main__':
    get_sales(engine)



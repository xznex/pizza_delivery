from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# postgresql://postgres:admin@localhost/pizza_delivery
engine = create_engine("postgresql://postgres:<username>:<password>@localhost/<db_name>", echo=True)
Base = declarative_base()
Session = sessionmaker()

import os
import sys
from sqlalchemy import create_engine
from db import Base
from sqlalchemy import URL

#'postgresql+psycopg2://user:password@hostname/database_name'
url_object = URL.create(
    "postgresql",
    username="postgres",
    password="password",
    host="localhost",
    database="postgres",
)

# "postgresql+pg8000://scott:tiger@localhost/test"
path = sys.argv[1]

# Creating an engine connecting to sqlite database - Enter your own path
# engine = create_engine(f"postgresql://srivinays:password@127.0.0.1:5432/postgres", echo = True)
engine = create_engine(f"sqlite:///{path}", echo = True)

# Creating the tables by calling the below function
Base.metadata.create_all(engine)    

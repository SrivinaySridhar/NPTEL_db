import os
import sys
from sqlalchemy import create_engine
from db import Base

path = sys.argv[1]

# Creating an engine connecting to sqlite database - Enter your own path
engine = create_engine(f"sqlite:///{path}", echo = True)

# Creating the tables by calling the below function
Base.metadata.create_all(engine)
# Setting the foreign key constraint on
os.system('sqlite3 f"{path}" "PRAGMA foreign_keys=ON"')
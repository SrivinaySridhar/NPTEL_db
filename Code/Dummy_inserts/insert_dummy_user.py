import datetime as dt
from sqlalchemy.orm import sessionmaker

import sys

sys.path.append('..')

from db import User
from run import engine

Session = sessionmaker(engine)
session = Session()

#Valid user
user1 = User(
    age_group = "20-30",
    dob = dt.date(2001, 7, 30),
    gender = "M",
    country = "India",
    state = "Tamil Nadu",
    city = "Chennai",
    pincode = 600017,
    qualification = "Higher Secondary",
    graduation_year = 2019,
    profession = "student",

    college_name = "IIT Madras",
    department = "Data Science",

    degree = "science",
    study_year = 3,
    scholarship = False,

    employer = "NPTEL",
    designation = "Data Analyst Intern",

    first_seen = dt.datetime.now(),
    last_updated = dt.datetime.now()
)

try:
    session.add(user1)
except:
    session.rollback()
    raise
else:
    session.commit()
finally:
    session.close()
  
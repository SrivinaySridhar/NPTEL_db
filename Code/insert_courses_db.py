from db import User, Enrolment, session
import datetime as dt

#Valid user
user1 = User(
    age_group = "20-30",
    dob = dt.date(2001, 7, 30),
    gender = "M",
    country = "India",
    state = "Tamil Nadu",
    city = "Chennai",
    qualification = "Higher Secondary",
    graduation_year = 2019,
    profession = "Student",

    college_name = "IIT Madras",
    local_chapter = True,
    college_id = 0,
    department = "Data Science",

    degree = "BS",
    study_year = "3rd year",
    scholarship = False,

    employer = "NPTEL",
    designation = "Data Analyst Intern",

    pwd_category = False,
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

#Valid course
#...

#Invalid course
#...   
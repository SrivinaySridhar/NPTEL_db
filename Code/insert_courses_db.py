from db import User, Course, Enrolment, session
import datetime as dt

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

    degree = "BS",
    study_year = 3,
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
course1 = Course(
    unique_course_id = 12345,
    course_run_id = "noc23_cs01",
    name = "Introduction to Python",
    discipline = "Computer Science",
    category = "Rerun",
    exam_date = dt.date(2023, 7, 30),
    duration = 12,
    faculty = "Prof. Sudarshan Iyengar",
    institute = "IIT Ropar",
    coordinating_institute = "IIT Madras",
    course_status = "op",
    is_fdp = True
)

try:
    session.add(course1)
except:
    session.rollback()
    raise
else:
    session.commit()

#Invalid course
#...   
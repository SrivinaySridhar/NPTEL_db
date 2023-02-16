from db import Course, session, engine
import datetime as dt

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

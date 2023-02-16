from db import Assignment, session
import datetime as dt

#Valid course
assignment1 = Assignment(
    course_run_id = "noc23_cs01",
    assignment_run_id = 101,
    week = 1,
    graded = True
)

try:
    session.add(assignment1)
except:
    session.rollback()
    raise
else:
    session.commit()
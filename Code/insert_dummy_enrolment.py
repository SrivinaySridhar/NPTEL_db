from db import Enrolment
from run import engine
import datetime as dt
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(engine)
session = Session()

#Valid course
enrolment1 = Enrolment(
    user_id = 1,
    course_run_id = 'noc23_cs01',
    date = dt.datetime.now(),
    first_seen = dt.datetime.now()
)

try:
    session.add(enrolment1)
except:
    session.rollback()
    raise
else:
    session.commit()

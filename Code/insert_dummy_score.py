from db import Score, session
import datetime as dt

#Valid course
score1 = Score(
    enrolment_id = 1,
    assignment_id = 1,
    score = 100
)

try:
    session.add(score1)
except:
    session.rollback()
    raise
else:
    session.commit()
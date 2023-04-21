from sqlalchemy.orm import sessionmaker

import sys

sys.path.append('..')

from db import Score
from run import engine

Session = sessionmaker(engine)
session = Session()

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
finally:
    session.close()
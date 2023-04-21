import datetime as dt
from sqlalchemy.orm import sessionmaker

import sys

sys.path.append('..')

from db import Registration
from run import engine

Session = sessionmaker(engine)
session = Session()

# Valid registration
registration1 = Registration(
    enrolment_id = 1,
    user_id = 1,
    payment_status = 'payment_complete',
    alloted_date_final = dt.datetime.now(),
    motivation = 'To update myself with knowledge in this field',
    information_source = 'Friends',
    share_course_with_orgs = True,
    # share_course_with_college = Null (Avoiding setting it to check if it takes null values)
    is_physically_challenged = False,
    is_sc_st = False,
    # pwd_category = Null (Avoiding setting it to check if it takes null values)
    # student_credit_transfer = Null (Avoiding setting it to check if it takes null values)
    first_state = "Tamil Nadu",
    first_city = "Chennai 1",
    second_state = "Tamil Nadu",
    second_city = "Chennai 2",
    third_state = "Tamil Nadu",
    third_city = "Chennai 3",
    transaction_date = dt.datetime.now()
)

try:
    session.add(registration1)
except:
    session.rollback()
    raise
else:
    session.commit()
finally:
    session.close()
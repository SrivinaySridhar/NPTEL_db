from db import User
from run import engine
import datetime as dt
from sqlalchemy.orm import sessionmaker
import csv
import sys

Session = sessionmaker(engine)
session = Session()

#-----------------------------------------x----------------------------------------------x-----------------------------------------

PATH_TO_USERS_CSV = sys.argv[2]

errors = []
report = {"inserted": 0, "failed": 0}
with open(PATH_TO_USERS_CSV, 'r', encoding="utf8") as file:
    csv_reader = csv.reader(file)
    next(csv_reader) # Skip 1st line as header
    for row in csv_reader:
        new_user = User(user_id = row[0],
                        age_group = row[1],
                        country = row[2],
                        state = row[3],
                        city = row[4],
                        qualification = row[5],
                        graduation_year = row[6],
                        profession = row[7],
                        college_name = row[8],
                        department = row[9],
                        degree = row[10],
                        study_year = row[11],
                        scholarship = row[12],
                        employer = row[13],
                        designation = row[14])
        try:    
            session.add(new_user)
            session.commit()
            report["inserted"] += 1
        except Exception as e:
            session.rollback()
            errors.append((row[0], e))
            report["failed"] += 1
            pass

# print("Errors in inserting the following users (course_run_id, error):", errors)
# print("Report of the insertion:", report)


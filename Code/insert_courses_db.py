from db import Course
from run import engine
import datetime as dt
from sqlalchemy.orm import sessionmaker
import csv
import sys

Session = sessionmaker(engine)
session = Session()

#-----------------------------------------x----------------------------------------------x-----------------------------------------

# Working code to insert all the cleaned course entries from the Courses.csv file 

# Number of entries inserted: 1211, Time taken to execute: 39.55s 

PATH_TO_COURSES_CSV = sys.argv[2]

errors = []
report = {"inserted": 0, "failed": 0}
with open(PATH_TO_COURSES_CSV, 'r', encoding="utf8") as file:
    csv_reader = csv.reader(file)
    next(csv_reader) # Skip 1st line as header
    for row in csv_reader:
        new_course = Course(unique_course_id = row[0],
                            course_run_id = row[1],
                            name =  row[2],
                            discipline = row[3],
                            category = row[4],
                            exam_date = dt.date.fromisoformat(row[5]),
                            duration = row[6], 
                            faculty = row[7], 
                            institute = row[8],
                            coordinating_institute = row[9], 
                            course_status = row[10], 
                            is_fdp = bool(row[11]))
        try:    
            session.add(new_course)
            session.commit()
            report["inserted"] += 1
        except Exception as e:
            session.rollback()
            errors.append((row[1], e))
            report["failed"] += 1
            pass

print("Errors in inserting the following courses (course_run_id, error):", errors)
print("Report of the insertion:", report)

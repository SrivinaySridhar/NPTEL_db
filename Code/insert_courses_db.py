from db import Course, engine
import datetime as dt
import pandas as pd
from sqlalchemy.orm import sessionmaker
import csv

Session = sessionmaker(engine)
session = Session()

#-----------------------------------------x----------------------------------------------x-----------------------------------------

# Working code to insert all the cleaned course entries from the ../Data/Courses.csv file 

# Number of entries inserted: 1211, Time taken to execute: 84.25s 

try:
    with open("../Data/Courses.csv", 'r', encoding="utf8") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            print(row)
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
            session.add(new_course)
            session.commit()
except:
    print("Error while trying to read the csv file or writing to database")

#-----------------------------------------x----------------------------------------------x-----------------------------------------

# # Working code to insert all the cleaned course entries from the ../Data/Courses.csv file 

# # Number of entries inserted: 1211, Time taken to execute: 84.25s 

# # course_objects = []
# with open("../Data/Courses.csv", 'r', encoding="utf8") as file:
#     csv_reader = csv.reader(file)
#     next(csv_reader)
#     for row in csv_reader:
#         print(row)
#         new_course = Course(unique_course_id = row[0],
#                             course_run_id = row[1],
#                             name =  row[2],
#                             discipline = row[3],
#                             category = row[4],
#                             exam_date = dt.date.fromisoformat(row[5]),
#                             duration = row[6], 
#                             faculty = row[7], 
#                             institute = row[8],
#                             coordinating_institute = row[9], 
#                             course_status = row[10], 
#                             is_fdp = bool(row[11]))
#         session.add(new_course)
#         session.commit()

#-----------------------------------------x----------------------------------------------x-----------------------------------------

# # Code to create a test.csv
# Few issues with strings and commas inside the csv file

# def create_test():
#     # Initializing the counter
#     i = 0

#     #open file1 in reading mode
#     courses = open("../Data/Courses.csv", 'r')

#     #open file2 in writing mode
#     test = open("../Data/test.csv",'w')

#     #read from file1 and write to file2
#     for line in courses:
#         if i % 10 == 0:
#             test.write(line)
#         i += 1 # Increment counter

#     #close file1 and file2
#     courses.close()
#     test.close()

#     #open file2 in reading mode
#     test = open('file2.txt','r')

#     #print the file2 content
#     print(test.read())

#     #close the file2
#     test.close()
        
#     return

# create_test()

#-----------------------------------------x----------------------------------------------x-----------------------------------------

# # file_id = '17SRD8Srf2h7_P0mxwaNDHWP117mIAlETN7KGj1EJazs' - for downloading from gdrive

# # # Creating a session to perform CRUD operations
# # session = sessionmaker()(bind = engine)

# # The following can be used to check the connection status
# pool = engine.pool

# # get the connections that are currently in use
# print("Connections in use:", pool.checkedin())

# # get the connections that are currently available in the pool
# print("Connections available:", pool.checkedout())

# try:
#     # Assign the cleaned course data to 'data'
#     data = prepare_course_data(COURSES_URL)
#     print(data)
# except:
#     print("Could not load the data")

# try:
#     # Create a connection
#     conn = engine.connect()

#     # get the connections that are currently in use
#     print("Connections in use:", pool.checkedin())

#     # get the connections that are currently available in the pool
#     print("Connections available:", pool.checkedout())

#     # Convert the data frame to sql and append it to the courses table
#     data.to_sql(name = "courses", con = engine, if_exists = 'append')
# except:
#     print("Could not append the data to the database")
# finally:
#     # Close the connection
#     conn.close()
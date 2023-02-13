from db import User, Course, Enrolment, session, engine
import datetime as dt
import pandas as pd
from time import time
from numpy import genfromtxt

# file_id = '17SRD8Srf2h7_P0mxwaNDHWP117mIAlETN7KGj1EJazs' - for downloading from gdrive

# Tried to write a function to read the file into a dataframe and convert it to SQL

# def prepare_course_data(file_name):

#     df = pd.read_csv(file_name)

#     df.rename(columns = {'NPTELCourseId':'unique_course_id', 'NOCCourseId':'course_run_id', 'NOCCourseName':'name',
#                         'discipline_name':'discipline', 'Category':'category', 'NOCExamDt1':'exam_date', 
#                         'duration (self-populated)':'duration', 'NOCCoordinatorNames':'faculty', 'NOCInstitute':'institute', 
#                         'nocCoordinatingInstitute':'coordinating_institute', 'CourseStatus':'course_status', 'FdpStatus':'is_fdp'},
#                         inplace = True)

      #Need to add code to generate the 'discipline' and 'duration' columns

#     df = df.loc[:, ['unique_course_id', 'course_run_id', 'name', 'discipline', 'category', 'exam_date', 'duration', 'faculty', 
#                     'institute', 'coordinating_institute', 'course_status', 'is_fdp']]

#     return

# prepare_course_data()

def Load_Data(file_name):
    data = pd.read_csv(file_name)
    return data

if __name__ == "__main__":
    t = time()

    try:
        file_name = "..\Data\Course_details_2022 - Courses_2022.csv"
        df = Load_Data(file_name)
    except:
        print("Could not load the data")
    
    try:
        df.rename(columns = {'NPTELCourseId':'unique_course_id', 'NOCCourseId':'course_run_id', 'NOCCourseName':'name',
                               'discipline_name':'discipline', 'Category':'category', 'NOCExamDt1':'exam_date', 
                               'duration (self-populated)':'duration', 'NOCCoordinatorNames':'faculty', 'NOCInstitute':'institute', 
                               'nocCoordinatingInstitute':'coordinating_institute', 'CourseStatus':'course_status', 'FdpStatus':'is_fdp'},
                               inplace = True)

        df = df.loc[:, ['unique_course_id', 'course_run_id', 'name', 'discipline', 'category', 'exam_date', 'duration', 'faculty', 
                    'institute', 'coordinating_institute', 'course_status', 'is_fdp']]
    
    except:
        print("Could not edit the data")
    
    #Bulk insert - Try to see if you can implement this


    #Was not using dataframes so have stopped working on it

    #         record = Course(**{
    #             'unique_course_id' : i[0],
    #             'course_run_id' : i[1],
    #             'name' : i[2],
    #             'discipline' : i[3],
    #             'category' : i[4],
    #             'exam_date' : dt.strptime(i[5], '%Y-%m-%d').date(),
    #             'duration' : i[6],
    #             'faculty' : i[7],
    #             'institute' : i[8],
    #             'coordinating_institute' : i[9],
    #             'is_fdp' : i[10]
    #         })
    #         session.add(record) #Add all the records

    #     session.commit() #Attempt to commit all the records
    # except:
    #     session.rollback() #Rollback the changes on error
    # finally:
    #     session.close() #Close the connection
    # print ("Time elapsed: " + str(time() - t) + " s.")

# #Valid user
# user1 = User(
#     age_group = "20-30",
#     dob = dt.date(2001, 7, 30),
#     gender = "M",
#     country = "India",
#     state = "Tamil Nadu",
#     city = "Chennai",
#     pincode = 600017,
#     qualification = "Higher Secondary",
#     graduation_year = 2019,
#     profession = "student",

#     college_name = "IIT Madras",
#     department = "Data Science",

#     degree = "BS",
#     study_year = 3,
#     scholarship = False,

#     employer = "NPTEL",
#     designation = "Data Analyst Intern",

#     pwd_category = False,
#     first_seen = dt.datetime.now(),
#     last_updated = dt.datetime.now()
# )

# try:
#     session.add(user1)
# except:
#     session.rollback()
#     raise
# else:
#     session.commit()

# #Valid course
# course1 = Course(
#     unique_course_id = 12345,
#     course_run_id = "noc23_cs01",
#     name = "Introduction to Python",
#     discipline = "Computer Science",
#     category = "Rerun",
#     exam_date = dt.date(2023, 7, 30),
#     duration = 12,
#     faculty = "Prof. Sudarshan Iyengar",
#     institute = "IIT Ropar",
#     coordinating_institute = "IIT Madras",
#     course_status = "op",
#     is_fdp = True
# )

# try:
#     session.add(course1)
# except:
#     session.rollback()
#     raise
# else:
#     session.commit()

# #Invalid course
# #...   
from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, Enum, Date, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime as dt

#Creating an engine connecting to sqlite database
engine = create_engine("sqlite:///courses.db", echo = True)

#Declarative style schema definition
Base = declarative_base()

#Foreign key support
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Everytime a connection to the engine is made, the "foreign keys" pragma is switched ON
#Add to Readme file - documentation.
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

#Users table
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer(), primary_key = True)
    age_group = Column(Enum(), nullable = False) #derived? Decide when we input data. Better to have
    dob = Column(Date()) #Nullable because users enter only during registration - Keep it for frontend
    gender = Column(Enum()) #Nullable because users enter only during registration
    country = Column(String(), nullable = False)
    state = Column(String(), nullable = False)
    city = Column(String(), nullable = False)
    pincode = Column(Integer(6)) #Nullable because users enter only during registration
    qualification = Column(Enum(), nullable = False)
    graduation_year = Column(Date(), nullable = False) #YYYY
    profession = Column(Enum(), nullable = False)

    #Following fields for profession = Faculty/Students
    college_name = Column(Enum()) #Look into the table that stores local_chapter to college name - Need the enum values - NPTEL team
    #The following can be derived from "college_name": 
    #"college_country", "college_state", "college_city", "local_chapter", "college_id"
    department = Column(String()) #Possible to make it Enum()? from NPTEL team

    #Following fields for profession = Students
    degree = Column(Enum()) #Need the enum values - NPTEL team
    study_year = Column(Integer())
    scholarship = Column(Boolean())

    #Following fields for profession = Employees
    employer = Column(String())
    designation = Column(String())

    #All
    pwd_category = Column(Boolean(), nullable = False)
    first_seen = Column(DateTime()) #Nullable? Is this data available? Yes. Useful?
    last_updated = Column(DateTime()) #Nullable? Can we somehow get this data?

    #Relationships
    enrolments = relationship("Enrolment")
    #Need the enum values for all the columns
    __table_args__ = (CheckConstraint(gender.in_(['M', 'F', 'O', None])), 
                      CheckConstraint(profession.in_(["student", "faculty", "employed", "other"])), 
                      CheckConstraint(age_group.in_(["13-20", "20-30", "30-40", "40-50", "50-60", "60-70", "70-80", "80-90", 
                                                     "90-100"])),
                      CheckConstraint(qualification.in_(['bachelor5yr', 'masters', 'diploma', 'high_school', 'bachelor4yr', 
                                                         'doctoral', 'pre_university', 'bachelor3yr', None])))

#Courses table
class Course(Base):
    __tablename__ = "courses"

    unique_course_id = Column(String(), nullable = False) #Alnum dtype
    course_run_id = Column(String(), primary_key = True, nullable = False) #Alnum dtype
    name = Column(String(), nullable = False)
    exam_date = Column(Date()) #Nullable? Do we have courses that do not have exams? Only one exam date for a course_run_id
    #year derived from exam date if needed
    term = Column(Enum(), nullable = False) #derived First half and second half
    #The duration of the course is available in assignment mapping sheet - Need to join with courses data and input here
    duration = Column(Integer(), nullable = False) #Changed to Enum because we know it can be 4/8/12 weeks course
    faculty = Column(String(), nullable = False) 
    institute = Column(Enum(), nullable = False) #Enum dtype because it can be one of the limited set of universities - NPTEL
    coordinating_institute = Column(Enum(), nullable = False) #Enum dtype because it can be one of the limited set of universities - NPTEL
    
    # #Discuss and decide whether the following fields should be added
    # category = Column(Enum(), nullable = False) #Can be New/Rerun - Add
    # course_status = Column(Enum(), nullable = False) #What is this? Can be op/uplc Understand and Rename 
    # is_fdp = Column(Boolean(), nullable = False) #Should we keep this here or in exam_registrations table? What does this mean?
    # discipline = Column(Enum(), nullable = False) #Should we add this or derive from course_run_id? Separate

    #Relationships
    enrolments = relationship("Enrolment")
    # assignments = relationship("Assignment") 

#Enrolments table
class Enrolment(Base):
    __tablename__ = "enrolments"

    #How to enforce that a user can register to a particular course only one time?
    #CheckConstraint on Table - for a course_run_id, user_id should be unique?
    enrolment_id = Column(Integer(), primary_key = True)
    user_id = Column(Integer(), ForeignKey("users.user_id"), nullable = False)
    course_run_id = Column(String(), ForeignKey("courses.course_run_id"), nullable = False) #Alnum dtype
    date = Column(DateTime(), default = dt.datetime.now(), nullable = False)
    #first_seen? - Useful

#Creating the tables by calling the below function
Base.metadata.create_all(engine)

#Creating a session to perform CRUD operations
session = sessionmaker()(bind = engine)
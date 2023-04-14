from sqlalchemy import Column, String, Integer, Boolean, Enum, Date, DateTime
from sqlalchemy import ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
# import datetime as dt

# Declarative style schema definition
Base = declarative_base()

# Foreign key support
from sqlalchemy.engine import Engine
from sqlalchemy import event

# Everytime a connection to the engine is made, the "foreign keys" pragma is switched ON
# Add to Readme file - documentation.
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

#Users table
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer(), primary_key = True)
    age_group = Column(Enum(), nullable = False) # derived? Decide when we input data. Better to have
    dob = Column(Date()) # Nullable because users enter only during registration - Keep it for frontend
    gender = Column(Enum()) # Nullable because users enter only during registration
    country = Column(String(), nullable = False)
    state = Column(String(), nullable = False)
    city = Column(String(), nullable = False)
    pincode = Column(Integer()) # Nullable because users enter only during registration
    qualification = Column(Enum(), nullable = False)
    graduation_year = Column(Integer(), nullable = False) # YYYY
    profession = Column(Enum(), nullable = False)

    # Following fields for profession = Faculty/Students
    college_name = Column(Enum()) # Look into the table that stores local_chapter to college name - Need the enum values - NPTEL team

    # The following can be derived from "college_name": 
    # "college_country", "college_state", "college_city", "local_chapter", "college_id"

    department = Column(String()) # Possible to make it Enum()? from NPTEL team

    # Following fields for profession = Students
    degree = Column(Enum(), nullable = False)
    study_year = Column(Integer())
    scholarship = Column(Boolean())

    # Following fields for profession = Employed
    employer = Column(String())
    designation = Column(String())

    # All
    pwd_category = Column(Boolean(), nullable = False)
    first_seen = Column(DateTime()) # Nullable? Is this data available? Yes. Useful?
    last_updated = Column(DateTime()) # Nullable? Can we somehow get this data?

    # Relationships
    courses_enroled = relationship("Enrolment", uselist = False, back_populates = "users")

    # Constraints for the table
    __table_args__ = (CheckConstraint(gender.in_(['M', 'F', 'O', None])), 
                      CheckConstraint(profession.in_(["student", "faculty", "employed", "other"])), 
                      CheckConstraint(age_group.in_(["13-20", "20-30", "30-40", "40-50", "50-60", "60-70", "70-80", "80-90", 
                                                     "90-100"])),
                      CheckConstraint(qualification.in_(['bachelor5yr', 'masters', 'diploma', 'high_school', 'bachelor4yr', 
                                                         'doctoral', 'pre_university', 'bachelor3yr', None])),
                      CheckConstraint(degree.in_(['diploma', 'btech', 'be', 'science', 'others', 'commerce_management', 
                                                  'medical', 'arts_humanities', 'mtech', 'phd', 'not_applicable', 'ms',
                                                  'me', 'dental' ]))) #have added dental from dropdown menu observation


# Courses table
class Course(Base):
    __tablename__ = "courses"

    unique_course_id = Column(Integer(), nullable = False) # Alnum dtype
    course_run_id = Column(String(), primary_key = True, nullable = False) # Alnum dtype
    name = Column(String(), nullable = False)
    discipline = Column(Enum(), nullable = False)
    category = Column(Enum(), nullable = False)
    exam_date = Column(Date()) # Nullable? 

    # The following can be derived from "exam_date": "year" and "term"(First half of the year and second half of the year)

    # The duration of the course is available in assignment mapping sheet - Need to join with courses data and input here
    duration = Column(Integer(), nullable = False)
    faculty = Column(String(), nullable = False) 
    institute = Column(Enum(), nullable = False) # Enum dtype because it can be one of the limited set of universities - NPTEL
    coordinating_institute = Column(Enum(), nullable = False) 
    course_status = Column(Enum(), nullable = False) # What is this? Can be op/uplc/uptc/upsc Understand and Rename 
    is_fdp = Column(Boolean(), nullable = False) 

    # Relationships
    students_enroled = relationship("Enrolment", uselist = False, back_populates = "course") # The list of students enrolled in the course
    course_assignments = relationship("Assignment") # The list of assignments of the course

    # Need the enum values for 'institute' column
    __table_args__ = (CheckConstraint(category.in_(['New', 'Rerun'])), 
                      CheckConstraint(duration.in_([4, 8, 12])), 
                      CheckConstraint(course_status.in_(["oc", "uplc", "uptc", "upsc"])),
                      CheckConstraint(coordinating_institute.in_(['IIT Kanpur', 'IIT Madras', 'IISc Bangalore', 'IIT Bombay', 
                                                                  'IIT Kharagpur', 'IIT Guwahati', 'IIT Roorkee', 'IIT Delhi'])))

# Enrolments table
class Enrolment(Base):
    __tablename__ = "enrolments"

    enrolment_id = Column(Integer(), primary_key = True)
    user_id = Column(Integer(), ForeignKey("users.user_id"), nullable = False)
    course_run_id = Column(String(), ForeignKey("courses.course_run_id"), nullable = False) # Alnum dtype
    date = Column(DateTime(), nullable = False) # default = dt.datetime.now()?
    first_seen = Column(DateTime(), nullable = False)

    users = relationship("User", back_populates = "courses_enroled")
    course = relationship("Course", back_populates = "students_enroled")

    # UniqueConstraint to enforce that each user can enrol to a particular course offered in a term only once
    __table_args__ = (UniqueConstraint('user_id', 'course_run_id', name='_user_course_run_uc'),)

# Assignments table
class Assignment(Base):
    __tablename__ = "assignments"

    assignment_id = Column(Integer(), primary_key = True)
    course_run_id = Column(String(), ForeignKey("courses.course_run_id"), nullable = False) # Alnum dtype
    assignment_run_id = Column(Integer(), nullable = False)
    week = Column(Integer(), nullable = False)
    graded = Column(Boolean(), nullable = False)

    # May or may not add:
    # deadline = Column(DateTime()) 
    # subjectivity = Column(Boolean(), nullable = False)

    # UniqueConstraint to enforce that each course_run and assignment_run pair is unique
    __table_args__ = (UniqueConstraint('course_run_id', 'assignment_run_id', name='_course_assignment_uc'), )

# Assignment scores table
class Score(Base):
    __tablename__ = "assignment_scores"

    enrolment_id = Column(String(), ForeignKey("enrolments.enrolment_id"), primary_key = True) # Alnum dtype
    assignment_id = Column(Integer(), ForeignKey("assignments.assignment_id"), primary_key = True)
    score = Column(Integer())

# Exam registrations table
class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer(), primary_key = True)
    enrolment_id = Column(String(), ForeignKey("enrolments.enrolment_id"), nullable = False)
    user_id = Column(Integer(), ForeignKey("users.user_id"), nullable = False)
    payment_status = Column(Enum(), nullable = False)
    alloted_date_final = Column(DateTime(), nullable = False)
    motivation = Column(Enum(), nullable = False)
    information_source = Column(Enum(), nullable = False)

    # Where is the information on the following column? Could not find it in the Registration data
    # alloted_slot = Column(Enum(), nullable = False)

    share_course_with_orgs = Column(Boolean(), nullable = True) # Null values for None in db
    share_course_with_college = Column(Boolean(), nullable = True) # Null values for None in db
    
    # The following column has all values as None. Should we add?
    # is_fdp_enabled = Column(Boolean(), nullable = False)

    is_physically_challenged = Column(Boolean(), nullable = False)
    is_sc_st = Column(Boolean(), nullable = False)
    pwd_category = Column(Enum(), nullable = True) # Null values for No in db
    student_credit_transfer = Column(Enum(), nullable = True) # Null values for None in db
    first_state = Column(String(), nullable = False)
    first_city = Column(String(), nullable = False)
    second_state = Column(String(), nullable = False)
    second_city = Column(String(), nullable = False)
    third_state = Column(String(), nullable = False)
    third_city = Column(String(), nullable = False)
    transaction_date = Column(DateTime(), nullable = False)

    __tableargs__ = (CheckConstraint(payment_status.in_(['payment_pending', 'payment_complete', 'payment_failed',
                                                         'payment_refund'])),
                    CheckConstraint(motivation.in_(['To update myself with knowledge in this field',
                                                    'Preparing for competitive exams',
                                                    'To learn about how MOOCs work',
                                                    'For getting a job/internship',
                                                    'For research purposes',
                                                    'Other'])),
                    CheckConstraint(information_source.in_(['College', 'NPTEL Localchapter', 'Internet', 
                                                            'Friends', 'Others'])),
                    CheckConstraint(student_credit_transfer.in_(['yes_and_share', 'no_and_share', 'no_and_no_share'])),
                    CheckConstraint(pwd_category.in_(['Learning Disability', 'Hearing Impaired',
                                                      'Orthopaedically Handicapped does not require elevator',
                                                      'Orthopaedically Handicapped requires elevator',
                                                      'Visually Impaired without scribe', 
                                                      'Visually Impaired with scribe'])))

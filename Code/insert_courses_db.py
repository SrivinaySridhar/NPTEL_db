from db import User, Course, Enrolment, engine
from clean_courses import prepare_course_data, COURSES_URL
import datetime as dt
import pandas as pd
from sqlalchemy.orm import sessionmaker


# file_id = '17SRD8Srf2h7_P0mxwaNDHWP117mIAlETN7KGj1EJazs' - for downloading from gdrive

# # Creating a session to perform CRUD operations
# session = sessionmaker()(bind = engine)

# The following can be used to check the connection status
pool = engine.pool

# get the connections that are currently in use
print("Connections in use:", pool.checkedin())

# get the connections that are currently available in the pool
print("Connections available:", pool.checkedout())

try:
    # Assign the cleaned course data to 'data'
    data = prepare_course_data(COURSES_URL)
except:
    print("Could not load the data")

try:
    # Create a connection
    conn = engine.connect()
    # Convert the data frame to sql and append it to the courses table
    data.to_sql(name = "courses", con = engine, if_exists = 'append')
except:
    print("Could not append the data to the database")
finally:
    # Close the connection
    conn.close()
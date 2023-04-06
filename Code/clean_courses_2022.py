import pandas as pd

COURSES_URL = '..\Data\Course_details_2022 - Courses_2022.csv'
DISCIPLINE_URL = '..\Data\Course_details_2022 - discipline.csv'
DURATION_URL = '..\Data\Course_details_2022 - duration.csv'

def Load_Data(file_name):
    data = pd.read_csv(file_name)
    return data

# A function to load the discipline mapping file and return a dictionary of the mapping 
def discipline_map(file_name):
    # Load the discipline data
    df_discipline = Load_Data(file_name)

    # Drop the diciplineid column
    df_discipline = df_discipline[['Disc_short_code','Discipline Name']]

    # Drop duplicate values
    df_discipline = df_discipline.drop_duplicates(subset = ['Disc_short_code'], keep = 'first')

    # Convert the df into a dictionary with the indices as the short code and the values as the full name
    discipline_mapping = df_discipline.set_index('Disc_short_code').T.to_dict('records')

    # Return the dictionary that is sitting inside this list
    return discipline_mapping[0]

# A function to load the duration mapping file and return a dictionary of the mapping 
def duration_map(file_name):
    # Load the duration data
    df_duration = Load_Data(file_name)

    # Three formats for the "Duration" column: (Only for 2022 data)
    # 1. "12 Weeks" - 
    # 2. "8 Weeks + 4 Weeks(New)"
    # 3. "4 Week(rerun) + 4 Week (New)"
    
    # The following function outputs different integer values according to the different formats
    # We can apply this to the "Duration" column, and can extract the integer values of the duration of each course
    func = lambda x : int(x[0:2]) + int(x[16:18]) if len(x) > 24 else (int(x[0:2]) + int(x[10:12]) if len(x) > 9 else int(x[0:2]))

    df_duration['_duration'] = df_duration['Duration'].apply(func)

    # Drop the diciplineid column
    df_duration = df_duration[['NOCCourseId','_duration']]

    # Convert the df into a dictionary with the indices as the short code and the values as the full name
    duration_mapping = df_duration.set_index('NOCCourseId').T.to_dict('records')

    # Return the dictionary that is sitting inside this list
    return duration_mapping[0]

#Read and clean the data before inserting into the database 
def prepare_course_data(file_name):
    
    # Load the data
    df = Load_Data(file_name)

    # How are we going to handle null values?

    # Rename the fields of the dataframe to match the fields of the courses table in the database
    df.rename(columns = {'NPTELCourseId':'unique_course_id', 'NOCCourseId':'course_run_id', 'NOCCourseName':'name',
                         'Category':'category', 'NOCExamDt1':'exam_date', 'NOCCoordinatorNames':'faculty', 
                         'NOCInstitute':'institute', 'nocCoordinatingInstitute':'coordinating_institute', 
                         'CourseStatus':'course_status', 'FdpStatus':'is_fdp'}, inplace = True)
    
    # Need to  derive '_discipline' and '_duration' columns. Note: Derived columns start with an '_'

    # Generate the '_discipline' column
    # Need to derive the short form of the discipline from the 'course_run_id'

    # Format of course_run_id: noc<YY>-<DD><NN(N)>
    # YY (Year), aa (discipline_short), NN(N) - Internal sequence number (Can be 2 or 3 digit)
    
    start, stop, step = 6, 8, 1 # start stop and step variables
    
    df["_discipline_short"]= df["course_run_id"].str.slice(start, stop, step)
    
    # Load the discipline map dictionary
    discipline_mapping = discipline_map(DISCIPLINE_URL)

    # Use the dictionary to derive the "_discipline" column
    df["_discipline"] = df['_discipline_short'].map(discipline_mapping)

    # Generate the '_duration' column
    # Use the 'duration_map(file_name)' function to get the mapping of the 'NOCCourseId' to '_duration

    # Load the duration map dictionary
    duration_mapping = duration_map(DURATION_URL)

    df['_duration'] = df['course_run_id'].map(duration_mapping)
    
    # Storing only the relevant columns and dropping the rest
    df = df.loc[:, ['unique_course_id', 'course_run_id', 'name', '_discipline', 'category', 'exam_date', '_duration', 'faculty', 
                    'institute', 'coordinating_institute', 'course_status', 'is_fdp']]
    
    # Drop those courses that do not have a duration value associated with it - Needed to convert to int
    df = df.dropna(axis=0, subset=['_duration'])

    # Converting the 'unique_course_id' and '_duration' to int() dtype
    df['unique_course_id'] = df['unique_course_id'].astype(int)
    df['_duration'] = df['_duration'].astype(int)
    
    # Converting 0s and 1s to Boolean values
    df['is_fdp'] = df['is_fdp'].astype(bool)

    # Converting date string to python date object
    df['exam_date'] = pd.to_datetime(df['exam_date'], format="%Y-%m-%d")

    # Returning the dataframe as a csv file
    df.to_csv('..\Data\Courses.csv', index = False, header = True)

    return

prepare_course_data(COURSES_URL)
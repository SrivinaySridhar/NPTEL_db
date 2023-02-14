import pandas as pd

def Load_Data(file_name):
    data = pd.read_csv(file_name)
    return data

# A function to load the discipline mapping file and return a dictionary of the mapping 
def discipline_map():
    df = Load_Data('..\Data\Course_details_2022 - discipline.csv')

    # Drop the diciplineid column
    df = df.drop(columns = ["disciplineid"])

    # Convert the df into a dictionary with the indices as the short code and the values as the full name
    discipline_mapping = df.set_index('Disc_short_code').T.to_dict('records')

    return discipline_mapping

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

    # Generate the 'discipline' column
    # Need to derive the short form of the discipline from the 'course_run_id'

    # Format of course_run_id: noc<YY>-<DD><NN(N)>
    # YY (Year), aa (discipline_short), NN(N) - Internal sequence number (Can be 2 or 3 digit)
    
    start, stop, step = 6, 8, 1 # start stop and step variables
    
    df["_discipline_short"]= df["course_run_id"].str.slice(start, stop, step)
    
    # Load the discipline map dictionary
    discipline_mapping = discipline_map()

    # Use the dictionary to derive the "_discipline" column
    # Need to refine: df["_discipline"] = discipline_mapping[df["_discipline_short"]]

    # Need to add code to generate the 'duration' column
    # ...
    
    # Storing only the relevant columns and dropping the rest
    df = df.loc[:, ['unique_course_id', 'course_run_id', 'name', 'discipline', 'category', 'exam_date', 'duration', 'faculty', 
                    'institute', 'coordinating_institute', 'course_status', 'is_fdp']]
    
    # Returning the dataframe
    return df

prepare_course_data()
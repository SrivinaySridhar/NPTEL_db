## How to create the database
> Note: All paths used should be complete paths.

Run the run.py script with the path to where you want to store the database 

```shell
python run.py "\path\to\db"
```
## [Link to DB data](https://drive.google.com/drive/folders/1E4eoLFFoUsh7HhKjhsQEJhHU9y7K_gf7?usp=share_link)

## How to clean the data 
In progress: Will modify to make it simpler - 1 input, 1 output. Can try to add the duration and discipline to the Course_details.csv beforehand - That will be the sole input.

### Important - Running this code drops the following courses:
1. noc22-ce88 
2. noc22-ch46

> Reason: The duration column could not be found for these two courses in the Assignment mapper file. The duration column of the database takes only `int` dtype and it cannot take null values, so these courses are dropped to avoid the error while inserting the courses. They can be manually inserted after ascertaining the right duration values. 

Run the clean_courses_2022.py with the following arguments:
1. Path to the Course_details_2022.csv
2. Path to the discipline.csv
3. Path to the duration.csv
4. Path to where you want to store the output (Courses.csv)

```shell
python clean_courses_2022.py         "\path\to\Course_details_2022.csv" 
"\path\to\discipline.csv"
"\path\to\duration.csv" 
"\path\to\Courses.csv"
```

## How to insert courses to the database
Run the insert_courses_db.py with the following arguments:
1. Path to the database
2. Path to Courses.csv (Cleaned courses file to be inserted)

```shell
python insert_courses_db.py "\path\to\db"             
                            "\path\to\Courses.csv"
```

# Database Schema
## Tables
### 1. Users
### 2. Courses
### 3. Enrolments
### 4. Assignments
### 5. Assignment Scores
### 6. Registrations

## Metadata of Tables

### 1. `users`

This table stores information about users of NPTEL.

Column|Type|Description
------|----|-----------
user_id| Integer| Primary key, Unique identifier for the user.
age_group| Enum| Age group of the user, restricted to specific ranges.
dob| Date| Date of birth of the user.
gender|	Enum|	Gender of the user, restricted to 'M', 'F', 'O' or NULL.
country|	String|	Country of residence of the user.
state|	String|	State of residence of the user.
city|	String|	City of residence of the user.
pincode|	Integer|	Postal code of the user's residence.
qualification|	Enum|	Highest educational qualification of the user.
graduation_year|	Integer|	Year of graduation for the user.
profession|	Enum|	Profession of the user, restricted to specific categories.
college_name|	Enum|	Name of the college the user is studies/teaches at.
department|	String|	Department the user studies/teaches.
degree|	Enum|	Type of degree earned by the user.
study_year|	Integer|	Year of study of the user.
scholarship|	Boolean|	Whether the user is receiving scholarship or not.
employer|	String|	Name of the employer of the user.
designation|	String|	Job designation of the user.
pwd_category|	Boolean|	Whether the user is a person with disability.
first_seen|	DateTime|	Date and time the user first signed into NPTEL.
last_updated|	DateTime|	Date and time the user's record was last updated.

### 2. `courses`

This table stores information about courses offered by NPTEL (past and current).

Column|	Type|	Description
------|-----|--------------
unique_course_id|	Integer|	Unique identifier for the course.
course_run_id|	String|	Primary key, Unique identifier for a specific offering of a course in a term.
name|	String|	Name of the course.
discipline|	Enum|	Discipline of the course.
category|	Enum|	New or Rerun category of the course.
exam_date|	Date|	Date of the exam for the course.
duration|	Integer|	Duration of the course in weeks.
faculty|	String|	Name of the faculty member teaching the course.
institute|	Enum|	Name of the institute offering the course.
coordinating_institute|	Enum|	Name of the coordinating institute for the course.
course_status|	Enum|	Status of the course.
is_fdp|	Boolean|	Whether the course is a Faculty Development Program or not.

### 3. `enrolments`

This table stores information about enrolments of users in specific offerings of courses.

Column|	Type|	Description
------|-----|--------------
enrolment_id|	Integer|	Primary key. Unique identifier for the enrolment.
user_id|	Integer|	Foreign key. Identifier for the user who enrolled in the course.
course_run_id|	String|	Foreign key. Identifier for the specific offering of the course.
date|	DateTime|	Date and time of enrolment.
first_seen|	DateTime|	Date and time the enrolment record was first created.

### 4. `assignments`

The assignments table stores information about assignments.

Column|	Type|	Description
------|-----|--------------
assignment_id|	Integer|	Primary key. Unique identifier for the assignment
course_run_id|	String|	Foreign key. Identifier of the course run associated with the assignment
assignment_run_id|	Integer| Identifier of the assignment run
week|	Integer|	Week in which the assignment is due
graded|	Boolean|	Indicates whether the assignment is graded or not

### 5. `assignement_scores`

The assignment_scores table stores information about assignment scores.

Column|	Type|	Description
------|-----|--------------
enrolment_id|	String|	Primary key, Foreign key.	Unique identifier of the enrolment associated with the assignment
assignment_id|	Integer| Primary key, Foreign key.	Unique identifier of the assignment associated with the enrolment
score|	Integer| The score achieved on the assignment

### 6. `registrations`

The registrations table stores information about the registrations for exams.

Column| Type|	Description
------|-----|--------------
id|	Integer| Primary Key, Unique identifier for each registration
enrolment_id| String|	Foreign Key, Identifier for enrolment, references enrolments table
user_id| Integer| Foreign Key, Identifier for user, references users table
payment_status|	Enum| Status of payment, can be 'payment_pending', 'payment_complete', 'payment_failed', or 'payment_refund'
alloted_date_final|	DateTime| Date and time of the final allotment
motivation|	Enum| Reason for taking the exam, can be 'To update myself with knowledge in this field', 'Preparing for competitive exams', 'To learn about how MOOCs work', 'For getting a job/internship', 'For research purposes', or 'Other'
information_source|	Enum| Source of information, can be 'College', 'NPTEL Localchapter', 'Internet', 'Friends', or 'Others'
share_course_with_orgs|	Boolean| Indicates whether to share the course with organizations
share_course_with_college| Boolean|	Indicates whether to share the course with the college
is_physically_challenged| Boolean| Indicates whether the candidate is physically challenged
is_sc_st| Boolean| Indicates whether the candidate belongs to a Scheduled Caste or Scheduled Tribe
pwd_category| Enum| Category of Physically Handicapped, can be 'Learning Disability', 'Hearing Impaired', 'Orthopaedically Handicapped does not require elevator', 'Orthopaedically Handicapped requires elevator', 'Visually Impaired without scribe', or 'Visually Impaired with scribe'
student_credit_transfer| Enum|	Indicates whether the student can transfer credits, can be 'yes_and_share', 'no_and_share', or 'no_and_no_share'
first_state| String| First preferred state where the candidate would prefer to take the exam
first_city| String| First preferred city where the candidate would prefer to take the exam
second_state| String| Second preferred state where the candidate would prefer to take the exam
second_city| String| Second preferred city where the candidate would prefer to take the exam
third_state| String| Third preferred state where the candidate would prefer to take the exam
third_city| String| Third preferred city where the candidate would prefer to take the exam
transaction_date| DateTime| Date and time of the transaction

## Relationships

### 1. ...
### 2. ...
### 3. ...

## Derived columns

### 1. ...
### 2. ...
### 3. ...

### Constraints

`assignments`


course_run_id references the course_runs table.
(_course_assignment_uc) UniqueConstraint to enforce that each course_run and assignment_run pair is unique.


`assignment_scores`

enrolment_id references the enrolments table.
assignment_id references the assignments table.
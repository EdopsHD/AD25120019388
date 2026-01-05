"""
This script performs various SQLite operations using Python. 
It connects to or creates a database file, creates a table, 
inserts multiple records, retrieves and updates data, deletes
a record, and finally drops the table and closes the connection.
"""

import sqlite3

# Connect to or create a SQLite database file
db = sqlite3.connect('student_db.db')

# Get a cursor object to interact with the database
cursor = db.cursor()

# Create the student table if it does not exist
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS student (
        id INTEGER PRIMARY KEY,
        name TEXT,
        grade INTEGER
    )
    '''
)

# Commit the changes to save the table creation
db.commit()

# Define data for students
students_data = [
    ('Andres', 60),
    ('John', 90),
    ('Sarah', 75)
]

# Insert multiple students into the table
cursor.executemany(
    '''
    INSERT INTO student(name, grade)
    VALUES(?, ?)
    ''',
    students_data
)
print('Multiple users inserted.\n')

# Commit the changes to save the inserted data
db.commit()

# Get the ID of the last inserted row
last_row_id = cursor.lastrowid
print(f'Last row ID: {last_row_id}\n')

# Retrieve and display data for the student with a specific ID
id = 3

# Execute query to fetch student with specific ID
cursor.execute('''SELECT name, grade FROM student WHERE id = ?''', (id,))

# Fetch the result of the query
student = cursor.fetchone()

# Print the student's details if found,
# otherwise output that no student was found
if student:
    print(f'Student with ID {id}: {student}\n')
else:
    print(f'No student found with ID {id}.\n')

# Retrieve all student records below a specific grade threshold
grade_threshold = 80

# Execute query to fetch students with grades below the threshold
cursor.execute(
    '''
    SELECT name, grade FROM student WHERE grade < ?
    ''', (grade_threshold,)
)

# Fetch all matching records
students = cursor.fetchall()

# Print each student's details if records are found,
# otherwise output that no students met the criteria.
if students:
    print(f'Students with a grade less than {grade_threshold}:')
    for student in students:
        print(f'{student[0]} : {student[1]}')
else:
    print(f'No students found with a grade less than {grade_threshold}.\n')

# Update the grade of the student with ID=1
grade = 100
id = 1

# Execute UPDATE statement to modify the student's grade
cursor.execute(
    '''
    UPDATE student SET grade = ? WHERE id = ?
    ''', (grade, id)
)

# Commit the changes to save the updated data
db.commit()

print(f'\nStudent with ID {id} updated with new grade {grade}.\n')

# Retrieve and display all students' names and grades
print('Updated student data:')

# Execute query to fetch all student records
cursor.execute('''SELECT name, grade FROM student''')

# Fetch all records
students = cursor.fetchall()

# Print each student's details if records are found, otherwise
# output that no data is available
if students:
    for row in students:
        print(f'{row[0]} : {row[1]}')
else:
    print('No student data available.\n')

# Delete the student with ID=2
id = 2

# Execute DELETE statement to remove student with specific ID
cursor.execute('''DELETE FROM student WHERE id = ?''', (id,))

# Commit the changes to save the deletion
db.commit()

print(f'\nStudent with ID {id} deleted.\n')

# Drop the 'student' table
cursor.execute('''DROP TABLE student''')
print('Student table deleted!\n')

# Commit the changes to save the table deletion
db.commit()

# Close the database connection
db.close()
print('Connection to database closed.')

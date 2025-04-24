from flask import Flask, jsonify, render_template, request
import sqlite3

app = Flask(__name__)

# Define the path to your SQLite database file
DATABASE = 'db/university.db'

def create_connection():
    conn = sqlite3.connect(DATABASE)
    return conn

# adding new student
# based off what he did in add book
@app.route('/api/add_student', methods=['POST'])
def add_student():
    try:
        data = request.get_json() # retrieves json data sent in request body
        student_id = data.get('StudentID') # gets value associated with key StudentID in json data and stores it in student_id
        name = data.get('Name') # same as above with name
        address = data.get('Address') # same as above with addresss
        conn = create_connection() # opens a connection to the sqlite db stored in var conn
        cursor = conn.cursor() # gets cursor object from db connection cursos used to execute SQL statements on db
        cursor.execute("INSERT INTO Student (StudentID, Name, Address) VALUES (?, ?, ?)",
                       (student_id, name, address)) # executes SQL insert that adds new record to student tablke with student_id, nae, address
        conn.commit() # commits changes to the db
        conn.close() # closes the connection
        return jsonify({'message': 'Student added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

# adding new course
# similar to add_student
@app.route('/api/add_course', methods=['POST'])
def add_course():
    try:
        data = request.get_json()
        course_id = data.get('CourseID')
        name = data.get('Name')
        credits = data.get('Credits')
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Course (CourseID, Name, Credits) VALUES (?, ?, ?)",
                       (course_id, name, credits))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Course added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

# adding new section
# similar to add_student
@app.route('/api/add_section', methods=['POST'])
def add_section():
    try:
        data = request.get_json()
        section_id = data.get('SectionID')
        course_id = data.get('CourseID')
        semester = data.get('Semester')
        year = data.get('Year')
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Section (SectionID, CourseID, Semester, Year) VALUES (?, ?, ?, ?)",
                       (section_id, course_id, semester, year))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Section added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

# list all the students
# based on get_all_books
@app.route('/api/students', methods=['GET'])
def get_all_students():
    try:
        conn = create_connection() # establishes the connection to db
        cursor = conn.cursor() # cursor is made from connection, used to execute sql commands/queries
        cursor.execute("SELECT * FROM Student") # selects all columns from student table and gets them all
        students = cursor.fetchall() # fetches all rows from query above and stores them in students variable
        conn.close() # closes connection
        student_list = [
            {'StudentID': s[0], 'Name': s[1], 'Address': s[2]} for s in students
        ] # conversts list of tuples in students into a list of dictionaries like get_all_books just different way of doing it using list comprehension
        return jsonify({'students': student_list}) # converts dictionary into list
    except Exception as e:
        return jsonify({'error': str(e)})

# list all the courses
@app.route('/api/courses', methods=['GET'])
def get_all_courses():
    try:
        rubric = request.args.get('rubric')
        conn = create_connection()
        cursor = conn.cursor()
        if rubric:
            query = "SELECT * FROM Course WHERE CourseID LIKE ?"
            cursor.execute(query, (f"{rubric}%",))
        else:
            cursor.execute("SELECT * FROM Course")
        courses = cursor.fetchall()
        conn.close()
        course_list = [
            {'CourseID': c[0], 'Name': c[1], 'Credits': c[2]} for c in courses
        ]
        return jsonify({'courses': course_list})
    except Exception as e:
        return jsonify({'error': str(e)})

# list all the sections
@app.route('/api/sections', methods=['GET'])
def get_all_sections():
    try:
        course_id = request.args.get('courseid')
        conn = create_connection()
        cursor = conn.cursor()
        if course_id:
            query = "SELECT * FROM Section WHERE CourseID = ?"
            cursor.execute(query, (course_id,))
        else:
            cursor.execute("SELECT * FROM Section")
        sections = cursor.fetchall()
        conn.close()
        section_list = [
            {'SectionID': s[0], 'CourseID': s[1], 'Semester': s[2], 'Year': s[3]} for s in sections
        ]
        return jsonify({'sections': section_list})
    except Exception as e:
        return jsonify({'error': str(e)})

# Render to render the index.html page
@app.route('/')
def index():
    return render_template('index.html')


#register a student in a section
@app.route('/api/register_student', methods=['POST'])
def register_student():
    data = request.json
    student_id = data.get('StudentID')
    section_id = data.get('SectionID')

    conn = create_connection()
    try:
        conn.execute(
            "INSERT INTO Registration (StudentID, SectionID) VALUES (?, ?)",
            (student_id, section_id)
        )
        conn.commit()
        return jsonify({'message': 'Student registered successfully'})
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Error: Student already registered or invalid ID'}), 400
    finally:
        conn.close()

#list all students in section
@app.route('/api/section_students')
def section_students():
    section_id = request.args.get('sectionid')

    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.StudentID, s.Name, s.Address
        FROM Student s
        JOIN Registration r ON s.StudentID = r.StudentID
        WHERE r.SectionID = ?
    """, (section_id,))
    students = cur.fetchall()
    conn.close()

    return jsonify({'students': [dict(zip([column[0] for column in cur.description], row)) for row in students]})

#list all courses a student has registered for
@app.route('/api/student_courses')
def student_courses():
    student_id = request.args.get('studentid')

    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT c.CourseID, c.Name, c.Credits
        FROM Course c
        JOIN Section sec ON c.CourseID = sec.CourseID
        JOIN Registration r ON r.SectionID = sec.SectionID
        WHERE r.StudentID = ?
    """, (student_id,))
    courses = cur.fetchall()
    conn.close()

    return jsonify({'courses': [dict(zip([column[0] for column in cur.description], row)) for row in courses]})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")


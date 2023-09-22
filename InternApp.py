# from curses import flash
# from flask_wtf.csrf import CSRFProtect, CSRFError
from io import BytesIO
from flask import Flask, render_template, request, redirect, flash, jsonify
from pymysql import connections
import os
import boto3
import botocore
from flask import send_file
# import pdfplumber
# Use BytesIO to handle the binary content
# from werkzeug.utils import secure_filename
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompwd,
    db=customdb

)

output = {}
table = 'Student'

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/homepage", methods=['GET', 'POST'])
def homepage():
    return render_template('home.html')

@app.route("/aboutpage", methods=['GET', 'POST'])
def aboutpage():
    return render_template('about.html')

@app.route("/featurepage", methods=['GET', 'POST'])
def featurepage():
    return render_template('feature.html')

@app.route("/contactpage", methods=['GET', 'POST'])
def contactpage():
    return render_template('contact.html')

@app.route("/coursepage", methods=['GET', 'POST'])
def coursepage():
    return render_template('course.html')

@app.route("/indexpage", methods=['GET', 'POST'])
def indexpage():
    return render_template('index.html')

@app.route("/teampage", methods=['GET', 'POST'])
def teampage():
    return render_template('team.html')

@app.route("/testimonialpage", methods=['GET', 'POST'])
def testimonialpage():
    return render_template('testimonial.html')

# @app.route("/studentInfo", methods=['GET', 'POST'])
# def studentInfo():
#     return render_template('display_studInfo.html')

# @app.route("/searchStudent", methods=['GET', 'POST'])
# def searchEmp():
#     return render_template('searchStudent.html')

# @app.route("/searchStudentProcess", methods=['GET', 'POST'])
# def searchEmpProcess():
#     stud_id = request.form['stud_id']

#     search_sql = "SELECT * FROM student WHERE Employee_ID=%s"
#     cursor = db_conn.cursor()

#     cursor.execute(search_sql, (stud_id))
#     rows = cursor.fetchall()
#     cursor.close()  

#     return render_template('student_info.html', rows=rows)


def authenticate_user(username, password):
    try:
        # Connection is db_conn !!!
        
        cursor = db_conn.cursor()
        cursor.execute("SELECT user_pass, upper(user_role) FROM users WHERE user_id = %s", (username,))
        user_data = cursor.fetchone()
        
        if user_data:
            db_pass, user_role = user_data
            
            # Check if password correct
            if password == db_pass:
                # Redirect users based on their roles
                if user_role == 'ADMIN':
                    return 'admin.html' # CHANGE BASED ON IMPLEMENTATION
                elif user_role == 'LECTURER':
                    return 'lecturer.html' # CHANGE BASED ON IMPLEMENTATION
                elif user_role == 'STUDENT':
                    return 'student.html' # CHANGE BASED ON IMPLEMENTATION
                elif user_role == 'COMPANY':
                    return 'company.html' # CHANGE BASED ON IMPLEMENTATION
                elif user_role == 'MASTER':
                    return 'home.html' # CHANGE BASED ON IMPLEMENTATION
                else:
                    return None  # Invalid user_role, access denied
        
        return None  # User not found or passwords don't match, access denied
    
    except Exception as e:
        print("Database error:", str(e))
        return None  # Access denied in case of an error
    
    finally:
        # Close the database connection
        if cursor:
            cursor.close()


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username'] #From index.html
    password = request.form['password'] #From index.html
    
    # Use your authenticate_user function here
    redirect_page = authenticate_user(username, password)
    
    if redirect_page:
        # Redirect to the appropriate page based on user role
        return render_template(redirect_page)
    else:
        return "Access denied"
    


@app.route("/displayStudInfo", methods=['GET', 'POST'])
def viewStudentInfo():
    statement = "SELECT s.* FROM student s JOIN company c ON s.com_id = c.com_id WHERE s.com_id = 'C0001';"
    cursor = db_conn.cursor()
    cursor.execute(statement)
    result = cursor.fetchall()
    cursor.close()
    
    return render_template('display_studInfo.html', data=result)

@app.route('/displayStudInfoDetails/<stud_id>')
def viewStudentInfoDetails(stud_id):
    statement = "SELECT * FROM student s WHERE stud_id = %s"
    cursor = db_conn.cursor()
    cursor.execute(statement, (stud_id,))
    result = cursor.fetchone()
            
    return render_template('display_studInfoDetails.html', student=result)


@app.route('/displayStudResume/<stud_id>')
def displayStudentResume(stud_id):
    statement = "SELECT stud_id, stud_resume FROM student s WHERE stud_id = %s"
    cursor = db_conn.cursor()
    cursor.execute(statement, (stud_id,))
    results = cursor.fetchone()
    
    if results: 
        studID, resume = results
        resume = "https://" + bucket + ".s3.amazonaws.com/stud_id-" + studID + "_pdf.pdf"
        return render_template('display_resume.html', results=results, resume=resume)
        
    else: 
        return "Invalid student."
        
    return render_template('display_studInfo.html')

# @app.route("/", methods=['GET', 'POST'])
# def home():
#     return render_template('AddEmp.html')


# @app.route("/about", methods=['POST'])
# def about():
#     return render_template('www.intellipaat.com')


# @app.route("/addemp", methods=['POST'])
# def AddEmp():
#     emp_id = request.form['emp_id']
#     first_name = request.form['first_name']
#     last_name = request.form['last_name']
#     pri_skill = request.form['pri_skill']
#     location = request.form['location']
#     emp_image_file = request.files['emp_image_file']

#     insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
#     cursor = db_conn.cursor()

#     if emp_image_file.filename == "":
#         return "Please select a file"

#     try:

#         cursor.execute(insert_sql, (emp_id, first_name, last_name, pri_skill, location))
#         db_conn.commit()
#         emp_name = "" + first_name + " " + last_name
#         # Uplaod image file in S3 #
#         emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
#         s3 = boto3.resource('s3')

#         try:
#             print("Data inserted in MySQL RDS... uploading image to S3...")
#             s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
#             bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
#             s3_location = (bucket_location['LocationConstraint'])

#             if s3_location is None:
#                 s3_location = ''
#             else:
#                 s3_location = '-' + s3_location

#             object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
#                 s3_location,
#                 custombucket,
#                 emp_image_file_name_in_s3)

#         except Exception as e:
#             return str(e)

#     finally:
#         cursor.close()

#     print("all modification done...")
#     return render_template('AddEmpOutput.html', name=emp_name)
    


@app.route("/lecturerDisplayStudInfo", methods=['GET', 'POST'])
def lecturerViewStudentInfo():
    statement = "SELECT s.* FROM student s JOIN lecturer l ON s.lec_id = l.lec_id WHERE s.lec_id = 'L0001';"
    cursor = db_conn.cursor()
    cursor.execute(statement)
    result = cursor.fetchall()
    cursor.close()
    
    return render_template('lec_displayStudInfo.html', data=result)


@app.route("/studProfile/<stud_id>", methods=['GET', 'POST'])
def GetStudInfo(stud_id):
    # Fetch student information from the database
    statement = "SELECT * FROM student s WHERE stud_id = %s"
    cursor = db_conn.cursor()
    cursor.execute(statement, (stud_id,))
    result = cursor.fetchone()
            
    return render_template('studProfile.html', student=result)
    
@app.route("/preview/<stud_id>")
def preview_file(stud_id):
    # Fetch the resume BLOB from the database
    cursor = db_conn.cursor()
    cursor.execute(f"SELECT stud_resume FROM Student WHERE stud_id = {stud_id}")
    resume_data = cursor.fetchone()
    cursor.close()

    if resume_data:
        # Save the resume to a temporary file
        resume_blob = resume_data[0]
        temp_file_path = f"temp_resume_{stud_id}.pdf"

        with open(temp_file_path, 'wb') as file:
            file.write(resume_blob)

        # Send the file for download
        return send_file(temp_file_path, as_attachment=True)
    else:
        return "Resume not found"


@app.route("/displayComInfo", methods=['GET', 'POST'])
def viewCompanyInfo():
    statement = "SELECT * FROM company WHERE status = 0;"
    cursor = db_conn.cursor()
    cursor.execute(statement)
    result = cursor.fetchall()
    cursor.close()
    
    return render_template('admin.html', data=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

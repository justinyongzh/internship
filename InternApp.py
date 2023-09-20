# from curses import flash
# from flask_wtf.csrf import CSRFProtect, CSRFError
from flask import Flask, render_template, request, redirect, flash, jsonify
from pymysql import connections
import os
import boto3
import botocore
# import pdfplumber
# Use BytesIO to handle the binary content
# from io import BytesIO
# from flask import send_file
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

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/homepage", methods=['GET', 'POST'])
def homepage():
    return render_template('home.html')

@app.route("studentInfo", methods=['GET', 'POST'])
def studentInfo():
    return render_template('display_studInfo.html')

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


@app.route("/display_studInfo", methods=['GET'])
def viewStudentInfo():
    statement = "SELECT s.* FROM student s JOIN Company c ON s.com_id = c.com_id WHERE s.com_id = 1;"
    cursor = db_conn.cursor()
    cursor.execute(statement)
    result = cursor.fetchall()
    return render_template('display_studInfo.html', data=result)

@app.route('/display_studInfoDetails/<stud_id>')
def viewStudentInfoDetails(stud_id):
    statement = "SELECT * FROM student s WHERE stud_id = %s"
    cursor = db_conn.cursor()
    cursor.execute(statement, (stud_id,))
    result = cursor.fetchone() #Assuming there's only one student with the given ID
            
    return render_template('display_studInfoDetails.html', student=result)

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)


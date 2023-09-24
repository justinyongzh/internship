# from curses import flash
# from flask_wtf.csrf import CSRFProtect, CSRFError
from io import BytesIO
from flask import Flask, render_template, session, request, redirect, flash, jsonify, url_for
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

@app.route("/searchStudentPage", methods=['GET', 'POST'])
def searchStudentPage():
    return render_template('comp_searchStudent.html')

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

@app.route("/adminViewCompanyPage", methods=['GET', 'POST'])
def adminViewCompanyPage():
    return render_template('admin.html')

@app.route("/ziyuPortfolio", methods=['GET', 'POST'])
def ziyuPortfolio():
    return render_template('ziyu_portfolio.html')

@app.route("/bingxinPortfolio", methods=['GET', 'POST'])
def bingxinPortfolio():
    return render_template('bingxin_portfolio.html')

@app.route("/justinPortfolio", methods=['GET', 'POST'])
def justinPortfolio():
    return render_template('justin_portfolio.html')

@app.route("/junxianPortfolio", methods=['GET', 'POST'])
def junxianPortfolio():
    return render_template('junxian_portfolio.html')

@app.route("/jianyongPortfolio", methods=['GET', 'POST'])
def jianyongPortfolio():
    return render_template('jianyong_portfolio.html')

@app.route("/xinyiPortfolio", methods=['GET', 'POST'])
def xinyiPortfolio():
    return render_template('xinyi_portfolio.html')

@app.route("/searchStudentProcess", methods=['GET', 'POST'])
def searchStudProcess():
    stud_id = request.form['stud_id']

    search_sql = "SELECT * FROM student WHERE stud_id = %s"
    cursor = db_conn.cursor()

    cursor.execute(search_sql, (stud_id))
    rows = cursor.fetchall()

    if rows:
        return render_template('comp_displaySearchStudInfo.html', rows=rows)
    else:
        return "Student does not exist."

    cursor.close()


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
                    return 'admin_home.html' # CHANGE BASED ON IMPLEMENTATION
                elif user_role == 'LECTURER':
                    return 'lecturer.html' # CHANGE BASED ON IMPLEMENTATION
                elif user_role == 'STUDENT':
                    return 'home.html' # CHANGE BASED ON IMPLEMENTATION
                elif user_role == 'COMPANY':
                    return 'home.html' # CHANGE BASED ON IMPLEMENTATION
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
        # Store the username in the Flask session
        session['username'] = username
        
        # Redirect to the appropriate page based on user role
        return render_template(redirect_page)
    else:
        return "Access denied"
    
@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))

@app.route('/signup', methods=['POST'])
def signup_post():
    username = request.form['signUpUsername'] #From index.html
    password = request.form['signUpPassword'] #From index.html
    roles    = request.form['roles'] #From index.html
    
    insert_sql = "INSERT INTO users VALUES (%s, %s, %s)"
    cursor = db_conn.cursor()
    cursor.execute(insert_sql, (username, password, roles))
    db_conn.commit()
    cursor.close()

    return render_template('index.html')

# @app.route("/displayStudInfo", methods=['GET', 'POST'])
# def viewStudentInfo():
#     statement = "SELECT s.* FROM student s JOIN company c ON s.com_id = c.com_id WHERE s.com_id = 'C0001';"
#     cursor = db_conn.cursor()
#     cursor.execute(statement)
#     result = cursor.fetchall()
#     cursor.close()
    
#     return render_template('display_studInfo.html', data=result)

@app.route("/displayStudInfo", methods=['GET', 'POST'])
def viewStudentInfo():
    username = session.get('username')

    if username:
        # statement = "SELECT s.* FROM student s JOIN company c ON s.com_email = c.com_email WHERE s.com_email = %s;"
        statement = "SELECT s.* FROM student s JOIN company c ON s.com_id = c.com_id WHERE s.com_id = %s;"

        cursor = db_conn.cursor()
        cursor.execute(statement, (username,))
        result = cursor.fetchall()
        cursor.close()

        return render_template('comp_displayStudInfo.html', data=result)
    
    else:
        return "Nothing found"

@app.route('/displayStudInfoDetails/<stud_id>')
def viewStudentInfoDetails(stud_id):
    statement = "SELECT * FROM student s WHERE stud_id = %s"
    cursor = db_conn.cursor()
    cursor.execute(statement, (stud_id,))
    result = cursor.fetchone()
            
    return render_template('comp_displayStudInfoDet.html', student=result)


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
        
    return render_template('comp_displayStudInfo.html')

@app.route("/lecturerDisplayStudInfo", methods=['GET', 'POST'])
def lecturerViewStudentInfo():
    statement = "SELECT s.* FROM student s JOIN lecturer l ON s.lec_id = l.lec_id WHERE s.lec_id = 'L0001';"
    cursor = db_conn.cursor()
    cursor.execute(statement)
    result = cursor.fetchall()
    cursor.close()
    
    return render_template('lec_displayStudInfo.html', data=result)


@app.route("/studProfile/", methods=['GET', 'POST'])
def GetStudInfo():
    username = session.get('username')

    if username:
        # Fetch student information from the database
        statement = "SELECT * FROM student WHERE stud_id = %s;"
        cursor = db_conn.cursor()
        cursor.execute(statement, (username,))
        student_data = cursor.fetchone()
        cursor.close()
    
        return render_template('studProfile.html', student=student_data)

    return "Student not found"


@app.route("/displayComInfo", methods=['GET', 'POST'])
def viewCompanyInfo():
    statement = "SELECT com_id,com_name,com_address,com_hp,com_email FROM company WHERE status = 0;"
    cursor = db_conn.cursor()
    cursor.execute(statement)
    result = cursor.fetchall()
    cursor.close()
    return render_template('admin.html', data=result)

@app.route('/delete_company/<com_email>', methods=['POST'])
def delete_company(com_email):
    company_email = request.form.get('com_email')
    statement = "DELETE FROM company WHERE com_email = %s;"
    cursor = db_conn.cursor()
    cursor.execute(statement, (com_email,))
    db_conn.commit()

    # Fetch the updated data from the database
    statement = "SELECT * FROM company WHERE status = 0"
    cursor.execute(statement)
    updated_data = cursor.fetchall()
    cursor.close()

    # Return the updated data as JSON
    return redirect(url_for('viewCompanyInfo'))

@app.route('/update_company_status/<com_email>', methods=['POST'])
def update_company_status(com_email):

        com_email = request.form.get('com_email')
        statement = "UPDATE company SET status = 1 WHERE com_email = %s;"
        cursor = db_conn.cursor()
        cursor.execute(statement, (com_email,))
        db_conn.commit()

        # Fetch the updated data from the database
        statement = "SELECT * FROM company WHERE status = 0"
        cursor.execute(statement)
        updated_data = cursor.fetchall()
        cursor.close()
        return redirect(url_for('viewCompanyInfo'))

# Function to fetch student data for editing
def get_student_data(stud_id):
    cursor = db_conn.cursor()
    cursor.execute(f"SELECT * FROM student WHERE stud_id = {stud_id}")
    student_data = cursor.fetchone()
    cursor.close()
    return student_data


# Route to edit student profile
@app.route("/editStudProfile/<stud_id>", methods=['GET', 'POST'])
def EditStudProfile(stud_id):
    username =  session.get('username')

    if username:
        if request.method == 'GET':
            statement = "SELECT * FROM student WHERE stud_id = %s;"
            cursor = db_conn.cursor()
            cursor.execute(statement, (username,))
            student_data = cursor.fetchone()
            cursor.close()

            return render_template('editStudProfile.html', student=student_data)
    

        elif request.method == 'POST':
            # Retrieve form data
            stud_name = request.form['stud_name']
            stud_programme = request.form['stud_programme']
            stud_mail = request.form['stud_mail']
            stud_HP = request.form['stud_HP']
            stud_ic = request.form['stud_ic']
            stud_gender = request.form['stud_gender']
            stud_currAddress = request.form['stud_currAddress']
            stud_homeAddress = request.form['stud_homeAddress']
            stud_resume = request.files['stud_resume']

            # Update the database with the new data
            cursor = db_conn.cursor()
            cursor.execute(f"UPDATE Student SET stud_name = '{stud_name}', stud_programme = '{stud_programme}', "
                        f"stud_email = '{stud_mail}', stud_HP = '{stud_HP}', stud_IC = '{stud_ic}', "
                        f"stud_gender = '{stud_gender}', stud_currAddress = '{stud_currAddress}', "
                        f"stud_homeAddress = '{stud_homeAddress}' WHERE stud_id = {stud_id}")
            db_conn.commit()
            cursor.close()

            # Check if a new resume file is provided
            if stud_resume.filename != "":
                s3 = boto3.resource('s3')
                stud_resume_name_in_s3 = "stud-id-" + str(stud_id) + "_resume.pdf"

                try:
                    s3.Bucket(custombucket).put_object(Key=stud_resume_name_in_s3, Body=stud_resume, ContentType='application/pdf')
                    bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
                    s3_location = (bucket_location['LocationConstraint'])

                    if s3_location is None:
                        s3_location = ''
                    else:
                        s3_location = '-' + s3_location

                    object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                        s3_location,
                        custombucket,
                        stud_resume_name_in_s3)
                    
                    # Update the stud_resume field in the database
                    cursor = db_conn.cursor()
                    cursor.execute(f"UPDATE student SET stud_resume = '{object_url}' WHERE stud_id = {stud_id}")
                    db_conn.commit()
                    cursor.close()

                except Exception as e:
                    return str(e)

            flash("Student profile updated successfully", "success")
            return redirect(url_for('GetStudInfo', stud_id=stud_id))
    
    return "Student not found"


if __name__ == '__main__':
    app.secret_key = 'cc_key'
    app.run(host='0.0.0.0', port=80, debug=True)

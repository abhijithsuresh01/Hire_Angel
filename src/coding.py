import functools
#wzdn tluy wafa kkzv
from flask import *
from src.dbconnectionnew import *
from flask_mail import *
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = "8978789494"


app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use the server for your mail service
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'angelhire7@gmail.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'wzdn tluy wafa kkzv'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = ('NURSE HIRING', 'angelhire7@gmail.com')

mail = Mail(app)


@app.route("/")
def login():
    return render_template("loginindex.html")

def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "lid" not in session:
            return render_template('loginindex.html')
        return func()

    return secure_function

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/nurse_registration")
def nurse_registration() :
    return render_template("Nurse/nursereg.html")
@app.route("/register_code", methods=['post'])
def register_code():
    fname=request.form["textfield"]
    lname = request.form["textfield2"]
    phone= request.form["textfield3"]
    email= request.form["textfield4"]
    nurseid = request.form["textfield5"]
    speciality=request.form["textfield6"]
    experience=request.form["textfield7"]
    username= request.form["textfield8"]
    password = request.form["textfield9"]
    resume = request.files['file']

    resume_name  = secure_filename(resume.filename)
    resume.save(os.path.join("static/uploads", resume_name))

    qry="INSERT INTO `login` VALUES (NULL, %s, %s,'pending')"
    val=(username,password)
    id=iud(qry, val)

    qry="INSERT INTO `nurses` VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(id,fname,lname,phone,email,nurseid,speciality,experience,resume_name)

    iud(qry, val)

    return '''<script>alert("successfully registered");window.location="/"</script>'''

@app.route("/hospital_registration")
def hospital_reg() :
    return render_template("Hospital/hospitalreg.html")

@app.route("/register_code_hsptl", methods=['post'])
def register_code_hsptl():
    fname=request.form["textfield"]

    location= request.form["textfield2"]
    contactno= request.form["textfield3"]
    email= request.form["email"]
    website = request.form["textfield4"]
    username= request.form["textfield5"]
    password = request.form["textfield6"]

    qry="INSERT INTO `login` VALUES (NULL, %s, %s,'pending')"
    val=(username,password)
    id=iud(qry, val)

    qry = "INSERT INTO `hospitals` VALUES (NULL,%s,%s,%s,%s,%s,%s)"
    val=(id,fname,location,contactno,website,email)

    iud(qry,val)

    return '''<script>alert("successfully registered");window.location="/"</script>'''




@app.route("/login_code", methods=['post'])
def login_code():
    username = request.form['textfield']
    password = request.form['textfield2']

    qry = "SELECT * FROM login WHERE username=%s AND password=%s"
    val = (username, password)
    res = selectone(qry, val)

    if res is None:
        return '''<script>alert("Invalid username or password");window.location="/"</script>'''
    elif res['type'] == "admin":
        session['lid'] = res['id']
        return '''<script>alert("Welcome Admin");window.location="/adminHome"</script>'''
    elif res['type'] == "nurse":
        session['lid'] = res['id']
        return '''<script>alert("Welcome Nurse");window.location="/nurseHome"</script>'''
    elif res['type'] == "hospital":
        session['lid'] = res['id']
        return '''<script>alert("Welcome Hospital");window.location="/hospitalHome"</script>'''
    else:
        return '''<script>alert("Invalid username or password");window.location="/"</script>'''

@app.route("/adminHome")
@login_required
def admin_home():
    return render_template("Admin/admin_index.html")
@app.route("/Verify_nurses")
@login_required
def Verify_nurses():

    qry = 'SELECT nurses.* FROM nurses JOIN login ON nurses.lid = login.id WHERE TYPE="pending"'
    res = selectall(qry)
    

    return render_template("Admin/nurse_view.html", val = res)


@app.route("/accept_nurse")
@login_required
def accept_nurse():
    id = request.args.get('id')
    qry = 'UPDATE login SET type="nurse" WHERE id=%s'
    iud(qry, id)

    qry = "SELECT * FROM `nurses` WHERE lid=%s"
    res = selectone(qry, id)

    def mail(email):
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('angelhire7@gmail.com', 'wzdn tluy wafa kkzv')
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText("You have been successfully accepted by admin")
        print(msg)
        msg['Subject'] = 'hey there'
        msg['To'] = email
        msg['From'] = 'angelhire7@gmail.com'
        try:
            gmail.send_message(msg)
        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))
        return '''<script>alert("SEND"); window.location="/"</script>'''

    mail(res['email'])

    return '''<script>alert("Successfully Accepted");window.location="/Verify_nurses"</script>'''


@app.route("/reject_nurse")
@login_required
def reject_nurse():
    id = request.args.get('id')
    qry = 'UPDATE login SET type="rejected" WHERE id=%s'
    iud(qry, id)

    qry = "SELECT * FROM `nurses` WHERE lid=%s"
    res = selectone(qry, id)

    def mail(email):
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('angelhire7@gmail.com', 'wzdn tluy wafa kkzv')
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText("You have been rejected by admin")
        print(msg)
        msg['Subject'] = 'hey there'
        msg['To'] = email
        msg['From'] = 'angelhire7@gmail.com'
        try:
            gmail.send_message(msg)
        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))
        return '''<script>alert("SEND"); window.location="/"</script>'''

    mail(res['email'])

    return '''<script>alert("Rejected");window.location="/Verify_nurses"</script>'''


@app.route("/Verify_hospital")
@login_required
def Verify_hospital():

    qry = 'SELECT hospitals.* FROM hospitals JOIN login ON hospitals.lid = login.id WHERE TYPE="pending"'
    res = selectall(qry)

    return render_template("Admin/hospital_view.html", val = res)


@app.route("/accept_hospital")
@login_required
def accept_hospital():
    id = request.args.get('id')
    qry = 'UPDATE login SET type="hospital" WHERE id=%s'
    iud(qry, id)

    qry = "SELECT * FROM `hospitals` WHERE lid=%s"
    res = selectone(qry, id)

    def mail(email):
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('angelhire7@gmail.com', 'wzdn tluy wafa kkzv')
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText("You have been successfully accepted by admin")
        print(msg)
        msg['Subject'] = 'hey there'
        msg['To'] = email
        msg['From'] = 'angelhire7@gmail.com'
        try:
            gmail.send_message(msg)
        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))
        return '''<script>alert("SEND"); window.location="/"</script>'''

    mail(res['email'])


    return '''<script>alert("Successfully Accepted");window.location="/Verify_hospital"</script>'''


@app.route("/reject_hospital")
@login_required
def reject_hospital():
    id = request.args.get('id')
    qry = 'UPDATE login SET type="rejected" WHERE id=%s'
    iud(qry, id)

    qry = "SELECT * FROM `hospitals` WHERE lid=%s"
    res = selectone(qry, id)

    def mail(email):
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('angelhire7@gmail.com', 'wzdn tluy wafa kkzv')
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText("You have been rejected by admin")
        print(msg)
        msg['Subject'] = 'hey there'
        msg['To'] = email
        msg['From'] = 'angelhire7@gmail.com'
        try:
            gmail.send_message(msg)
        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))
        return '''<script>alert("SEND"); window.location="/"</script>'''

    mail(res['email'])

    return '''<script>alert("Rejected");window.location="/Verify_hospital"</script>'''


@app.route("/blockUnblockNurse")
@login_required
def blockUnblockNurse():
    qry = 'SELECT * FROM nurses JOIN login ON nurses.lid = login.id WHERE type="nurse" or type="blocked"'
    res = selectall(qry)
    return render_template("Admin/blocknurse.html", val=res)


@app.route("/block_nurse")
@login_required
def block_nurse():
    id = request.args.get('id')
    qry = 'UPDATE login SET type= "blocked" WHERE id=%s'
    iud(qry, id)

    qry = "SELECT * FROM `nurses` WHERE lid=%s"
    res = selectone(qry, id)

    def mail(email):
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('angelhire7@gmail.com', 'wzdn tluy wafa kkzv')
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText("Hi "+ res['fname'] +",You have been blocked by admin")
        print(msg)
        msg['Subject'] = 'hey there'
        msg['To'] = email
        msg['From'] = 'angelhire7@gmail.com'
        try:
            gmail.send_message(msg)
        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))
        return '''<script>alert("SEND"); window.location="/"</script>'''

    mail(res['email'])

    return '''<script>alert("Blocked");window.location="/blockUnblockNurse"</script>'''

@app.route("/unblock_nurse")
@login_required
def unblock_nurse():
    id = request.args.get('id')
    qry = 'UPDATE login SET type= "nurse" WHERE id=%s'
    iud(qry, id)

    qry = "SELECT * FROM `nurses` WHERE lid=%s"
    res = selectone(qry, id)

    def mail(email):
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('angelhire7@gmail.com', 'wzdn tluy wafa kkzv')
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText("Hi "+ res['fname'] +",You have been unblocked by admin")
        print(msg)
        msg['Subject'] = 'hey there'
        msg['To'] = email
        msg['From'] = 'angelhire7@gmail.com'
        try:
            gmail.send_message(msg)
        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))
        return '''<script>alert("SEND"); window.location="/"</script>'''

    mail(res['email'])

    return '''<script>alert("Unblocked");window.location="/blockUnblockNurse"</script>'''


@app.route("/blockUnblockHospital")
@login_required
def blockUnblockHospital():
    qry = 'SELECT * FROM hospitals JOIN login ON hospitals.lid = login.id WHERE type="hospital" or type="blocked"'
    res = selectall(qry)
    return render_template("Admin/blockhospital.html", val=res)


@app.route("/block_hospital")
@login_required
def block_hospital():
    id = request.args.get('id')
    qry = 'UPDATE login SET type= "blocked" WHERE id=%s'
    iud(qry, id)

    qry = "SELECT * FROM `hospitals` WHERE lid=%s"
    res = selectone(qry, id)

    def mail(email):
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('angelhire7@gmail.com', 'wzdn tluy wafa kkzv')
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText("Hi "+ res['name'] +",You have been blocked by admin")
        print(msg)
        msg['Subject'] = 'hey there'
        msg['To'] = email
        msg['From'] = 'angelhire7@gmail.com'
        try:
            gmail.send_message(msg)
        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))
        return '''<script>alert("SEND"); window.location="/"</script>'''

    mail(res['email'])


    return '''<script>alert("Blocked");window.location="/blockUnblockHospital"</script>'''

@app.route("/unblock_hospital")
@login_required
def unblock_hospital():
    id = request.args.get('id')
    qry = 'UPDATE login SET type= "hospital" WHERE id=%s'
    iud(qry, id)

    qry = "SELECT * FROM `hospitals` WHERE lid=%s"
    res = selectone(qry, id)

    def mail(email):
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('angelhire7@gmail.com', 'wzdn tluy wafa kkzv')
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText("Hi "+ res['name'] +", You have been unblocked by admin")
        print(msg)
        msg['Subject'] = 'hey there'
        msg['To'] = email
        msg['From'] = 'angelhire7@gmail.com'
        try:
            gmail.send_message(msg)
        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))
        return '''<script>alert("SEND"); window.location="/"</script>'''

    mail(res['email'])

    return '''<script>alert("Unblocked");window.location="/blockUnblockHospital"</script>'''



@app.route("/viewcomplaints")
@login_required
def viewcomplaints():
    return render_template("Admin/complaint.html")


@app.route("/display_complaints", methods=['post'])
@login_required
def display_complaints():
    c_type = request.form['select']
    u_type = request.form['select2']
    if c_type == "Pending":
        if u_type == "Nurse":
            qry = "SELECT `nurses`.`fname`,`lname`,`complaints`.* FROM `complaints` JOIN `nurses` ON `complaints`.`lid` = `nurses`.`lid` WHERE `complaints`.`reply`='pending'"
            res = selectall(qry)
            return render_template("Admin/complaint.html", val = res, ctype=c_type, utype = u_type)
        else:
            qry = "SELECT `hospitals`.`name`, `complaints`.* FROM `complaints` JOIN `hospitals` ON `complaints`.`lid`=`hospitals`.`lid` WHERE `complaints`.`reply`='pending'"
            res = selectall(qry)
            return render_template("Admin/complaint.html", val=res, ctype=c_type, utype=u_type)
    else:
        if u_type == "Nurse":
            qry = "SELECT `nurses`.`fname`,`lname`,`complaints`.* FROM `complaints` JOIN `nurses` ON `complaints`.`lid` = `nurses`.`lid` WHERE `complaints`.`reply`!='pending'"
            res = selectall(qry)
            return render_template("Admin/complaint.html", val = res, ctype=c_type, utype = u_type)
        else:
            qry = "SELECT `hospitals`.`name`, `complaints`.* FROM `complaints` JOIN `hospitals` ON `complaints`.`lid`=`hospitals`.`lid` WHERE `complaints`.`reply`!='pending'"
            res = selectall(qry)
            return render_template("Admin/complaint.html", val=res, ctype=c_type, utype=u_type)



@app.route("/complaintreply")
@login_required
def complaintreply():

    id = request.args.get('id')
    session['cid'] = id

    return render_template("Admin/complaintreply.html")


@app.route("/insert_reply", methods=['post'])
@login_required
def insert_reply():
    reply = request.form['textfield']
    qry = "UPDATE complaint SET reply = %s WHERE id = %s"
    iud(qry,(reply, session['cid']))
    return render_template("Admin/complaintreply.html")


@app.route("/display_complaint", methods=['post'])
@login_required
def display_complaint():
    complaint_type = request.form['select']
    user_type = request.form['select2']

    if complaint_type == "Pending":
        if user_type == "nurse":
            qry = 'SELECT * FROM complaints JOIN nurses ON complaints.lid=nurses.lid WHERE complaints.reply="pending"'
            res = selectall(qry)
            return render_template("Admin/complaintreply.html", val=res, utype = user_type, ctype = complaint_type)
        else:
            qry = 'SELECT * FROM complaints JOIN hospitals ON complaints.lid=hospitals.lid WHERE complaints.reply="pending"'
            res = selectall(qry)
            return render_template("Admin/complaintreply.html", val=res, utype = user_type, ctype = complaint_type)
    else:
        if user_type == "nurses":
            qry = 'SELECT * FROM complaints JOIN nurses ON complaints.lid=nurses.lid WHERE complaints.reply!="pending"'
            res = selectall(qry)
            return render_template("Admin/complaintreply.html", val=res, utype = user_type, ctype = complaint_type)
        else:
            qry = 'SELECT * FROM complaints JOIN hospitals ON complaints.lid=hospitals.lid WHERE complaints.reply!="pending"'
            res = selectall(qry)
            return render_template("Admin/complaintreply.html", val=res, utype = user_type, ctype = complaint_type)



@app.route("/viewHospital")
@login_required
def view_hospital():
    return render_template("Admin/hospital_view.html")

@app.route("/viewNurse")
@login_required
def view_nurse():
    return render_template("Admin/nurse_view.html")

@app.route("/nurseHome")
@login_required
def nurse_home():
    return render_template("Nurse/nurse_index.html")

@app.route("/regNurse")

def reg_nurse():
    return render_template("Nurse/nursereg.html")

@app.route("/jobApply")
@login_required
def job_apply():
    qry = "SELECT `hospitals`.`name` AS hname, `job details`.* FROM `job details` JOIN `hospitals` ON `job details`.`hospital_id`=`hospitals`.`lid`"
    res = selectall(qry)
    return render_template("Nurse/apply_job.html", val=res)

@app.route("/jobStatus")
@login_required
def job_status():
    qry = "SELECT `job details`.name, `job application`.* FROM `job application` JOIN `job details` ON `job application`.`job_id`=`job details`.`id` WHERE `job application`.`nurse_id`=%s"
    res = selectall2(qry, session['lid'])
    return render_template("Nurse/job_status.html", val = res)

@app.route("/addComplaintsNurse")
@login_required
def add_complaints_nurse():
    qry = "SELECT * FROM `complaints` WHERE `lid`=%s"
    res = selectall2(qry, session['lid'])
    return render_template("Nurse/complaints.html", val=res)

@app.route("/viewComplaintsNurse", methods=['post'])
@login_required
def view_complaints_nurse():
    return render_template("Nurse/view_complaints.html")


@app.route("/insert_complaint", methods=['post'])
@login_required
def insert_complaint():
    complaint = request.form['textfield']
    qry = "INSERT INTO `complaints` VALUES(NULL,%s,%s,'pending',CURDATE())"
    iud(qry, (session['lid'], complaint))

    return '''<script>alert("Success");window.location="addComplaintsNurse"</script>'''


@app.route("/apply_job")
@login_required
def apply_job():
    id = request.args.get('id')

    qry = "SELECT * FROM `job application` WHERE `job_id`=%s and nurse_id=%s"
    res = selectone(qry, (id, session['lid']))

    if res is None:

        qry = "INSERT INTO `job application` VALUES(NULL,%s,%s,'pending',CURDATE())"
        id = iud(qry, (session['lid'],id))

        if session['file']!="no":

            qry = "INSERT INTO `equivalency` VALUES(NULL, %s, %s)"
            iud(qry,(id, session['file']))

        session['file'] = "no"


        return '''<script>alert("Success");window.location="jobApply"</script>'''
    else:
        return '''<script>alert("Already applied");window.location="jobApply"</script>'''


@app.route("/manage_review")
@login_required
def manage_review():
    qry = "SELECT `hospitals`.name,`reviews`.* FROM `reviews` JOIN `hospitals` ON `reviews`.`hospital_id`=`hospitals`.lid WHERE `reviews`.`nurse_id`=%s"
    res = selectall2(qry, session['lid'])
    return render_template("Nurse/manage_review.html", val = res)


@app.route("/add_review", methods=['post'])
@login_required
def add_review():
    qry = "SELECT * FROM `hospitals` JOIN `login` ON `hospitals`.lid=`login`.id WHERE `login`.type='hospital'"
    res = selectall(qry)
    return render_template("Nurse/add_review.html", val = res)


@app.route("/insert_review", methods=['post'])
@login_required
def insert_review():
    hid = request.form['select']
    review = request.form['textfield']
    qry = "INSERT INTO `reviews` VALUES(NULL, %s, %s, %s, CURDATE())"
    iud(qry,(session['lid'], hid, review))
    return '''<script>alert("Success");window.location="manage_review"</script>'''


@app.route("/hospitalHome")
def hospital_home():
    return render_template("Hospital/hospital_index.html")

@app.route("/regHospital")

def reg_hospital():
    return render_template("Hospital/hospitalreg.html")
@app.route("/addJob")
def addjob() :
    return render_template("Hospital/add_job.html")

@app.route("/addJobcode", methods=['post'])
def add_Jobcode():
    jobname =request.form["textfield"]
    details =request.form["textfield2"]
    date =request.form["textfield3"]
    criteria =request.form["textfield4"]

    qry= "INSERT INTO `job details` VALUES (NULL,%s,%s,%s,%s,%s)"
    iud(qry, (session['lid'],jobname,details,date,criteria))
    return '''<script>alert("JOB ADDED SUCCESFULLY");window.location="/addJob"</script>'''
@app.route("/manageJob")
def manage_job():
    qry="SELECT * FROM `job details` WHERE hospital_id=%s"

    res=selectall2(qry,session['lid'])

    return render_template("Hospital/manage_job.html",val=res)


@app.route("/delete_job")
@login_required
def delete_job():
    id = request.args.get('id')
    print(id)
    qry = 'DELETE FROM `job details` WHERE id=%s'
    iud(qry, id)
    return '''<script>alert("Successfully Deleted");window.location="/manageJob"</script>'''



@app.route("/jobapplications")
@login_required
def job_applications():
    qry = "SELECT `nurses`.`fname`,`lname`,`experience`,`resume`,`job details`.*,`job application`.id AS jaid FROM `job application` JOIN `job details` ON `job application`.`job_id`=`job details`.id JOIN `nurses` ON `job application`.`nurse_id`=`nurses`.lid WHERE `job details`.`hospital_id`=%s and `job application`.`status`='pending'"
    res = selectall2(qry,session['lid'])
    return render_template("Hospital/job_applications.html", val=res)


@app.route("/accept_job")
@login_required
def accept_job():
    id = request.args.get('id')
    qry = 'UPDATE `job application` SET status="accepted" WHERE id=%s'
    iud(qry, id)
    return '''<script>alert("Successfully Accepted");window.location="/jobapplications"</script>'''



@app.route("/reject_job")
@login_required
def reject_job():
    id = request.args.get('id')
    qry = 'UPDATE `job application` SET status="rejected" WHERE id=%s'
    iud(qry, id)
    return '''<script>alert("Successfully Rejected");window.location="/jobapplications"</script>'''


@app.route("/addComplaintsHospital")
@login_required
def addComplaintsHospital():
    qry = "SELECT * FROM `complaints` WHERE `lid`=%s"
    res = selectall2(qry, session['lid'])
    return render_template("Hospital/complaints.html", val=res)

    return render_template("Hospital/complaints.html")

@app.route("/viewComplaintsHospital", methods=['post'])
@login_required
def viewComplaintsHospital():
    return render_template("Hospital/view_complaint.html")

@app.route("/hospital_insert_complaint", methods=['post'])
@login_required
def hospital_insert_complaint():
    complaint = request.form['textfield']
    qry = "INSERT INTO `complaints` VALUES(NULL,%s,%s,'pending',CURDATE())"
    iud(qry, (session['lid'], complaint))

    return '''<script>alert("Success");window.location="addComplaintsHospital"</script>'''


@app.route("/add_equi")
def add_equi():
    return render_template("Nurse/equi.html")


@app.route("/insert_equi", methods=['post'])
def insert_equi():
    file = request.files['equi']

    file_name = secure_filename(file.filename)
    file.save(os.path.join("static/uploads", file_name))

    session['file'] = file_name

    return redirect("/jobApply")


@app.route("/view_equi")
def view_equi():
    id = request.args.get('id')
    qry = "SELECT * FROM `equivalency` WHERE `j_apply_id`=%s"
    res = selectall2(qry, id)

    return render_template("Hospital/view_equi.html", val=res)


if __name__ == "__main__":
    app.run(debug=True)

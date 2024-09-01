from flask import *
from src.dbconnectionnew import *
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

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
    website = request.form["textfield4"]
    username= request.form["textfield5"]
    password = request.form["textfield6"]

    qry="INSERT INTO `login` VALUES (NULL, %s, %s,'pending')"
    val=(username,password)
    id=iud(qry, val)

    qry = "INSERT INTO `hospitals` VALUES (NULL,%s,%s,%s,%s,%s)"
    val=(id,fname,location,contactno,website)

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
        return '''<script>alert("Welcome Admin");window.location="/adminHome"</script>'''
    elif res['type'] == "nurse":
        return '''<script>alert("Welcome Nurse");window.location="/nurseHome"</script>'''
    elif res['type'] == "hospital":
        return '''<script>alert("Welcome Hospital");window.location="/hospitalHome"</script>'''
    else:
        return '''<script>alert("Invalid username or password");window.location="/"</script>'''

@app.route("/adminHome")
def admin_home():
    return render_template("Admin/adminhome.html")
@app.route("/Verify_nurses")
def Verify_nurses():

    qry = 'SELECT nurses.* FROM nurses JOIN login ON nurses.lid = login.id WHERE TYPE="pending"'
    res = selectall(qry)

    return render_template("Admin/nurse_view.html", val = res)


@app.route("/accept_nurse")
def accept_nurse():
    id = request.args.get('id')
    qry = 'UPDATE login SET type="nurse" WHERE id=%s'
    iud(qry, id)
    return '''<script>alert("Successfully Accepted");window.location="/Verify_nurses"</script>'''


@app.route("/reject_nurse")
def reject_nurse():
    id = request.args.get('id')
    qry = 'UPDATE login SET type="rejected" WHERE id=%s'
    iud(qry, id)
    return '''<script>alert("Rejected");window.location="/Verify_nurses"</script>'''


@app.route("/Verify_hospital")
def Verify_hospital():

    qry = 'SELECT hospitals.* FROM hospitals JOIN login ON hospitals.lid = login.id WHERE TYPE="pending"'
    res = selectall(qry)

    return render_template("Admin/hospital_view.html", val = res)


@app.route("/accept_hospital")
def accept_hospital():
    id = request.args.get('id')
    qry = 'UPDATE login SET type="hospital" WHERE id=%s'
    iud(qry, id)
    return '''<script>alert("Successfully Accepted");window.location="/Verify_hospital"</script>'''


@app.route("/reject_hospital")
def reject_hospital():
    id = request.args.get('id')
    qry = 'UPDATE login SET type="rejected" WHERE id=%s'
    iud(qry, id)
    return '''<script>alert("Rejected");window.location="/Verify_hospital"</script>'''


@app.route("/blockUnblockNurse")
def blockUnblockNurse():
    qry = 'SELECT * FROM nurses JOIN login ON nurses.lid = login.id WHERE type="nurse" or type="blocked"'
    res = selectall(qry)
    return render_template("Admin/blocknurse.html", val=res)


@app.route("/block_nurse")
def block_nurse():
    id = request.args.get('id')
    qry = 'UPDATE login SET type= "blocked" WHERE id=%s'
    iud(qry, id)
    return '''<script>alert("Blocked");window.location="/blockUnblockNurse"</script>'''

@app.route("/unblock_nurse")
def unblock_nurse():
    id = request.args.get('id')
    qry = 'UPDATE login SET type= "nurse" WHERE id=%s'
    iud(qry, id)
    return '''<script>alert("Unblocked");window.location="/blockUnblockNurse"</script>'''


@app.route("/blockUnblockHospital")
def blockUnblockHospital():
    qry = 'SELECT * FROM hospitals JOIN login ON hospitals.lid = login.id WHERE type="hospital" or type="blocked"'
    res = selectall(qry)
    return render_template("Admin/blockhospital.html", val=res)


@app.route("/block_hospital")
def block_hospital():
    id = request.args.get('id')
    qry = 'UPDATE login SET type= "blocked" WHERE id=%s'
    iud(qry, id)
    return '''<script>alert("Blocked");window.location="/blockUnblockHospital"</script>'''

@app.route("/unblock_hospital")
def unblock_hospital():
    id = request.args.get('id')
    qry = 'UPDATE login SET type= "hospital" WHERE id=%s'
    iud(qry, id)
    return '''<script>alert("Unblocked");window.location="/blockUnblockHospital"</script>'''



@app.route("/viewcomplaints")
def viewcomplaints():
    return render_template("Admin/complaint.html")


@app.route("/complaintreply")
def complaintreply():

    return render_template("Admin/complaintreply.html")


@app.route("/insert_reply", methods=['post'])
def insert_reply():
    reply = request.form['textfield']
    qry = "UPDATE complaint SET reply = %s WHERE id = %s"
    iud(qry,(reply, session['cid']))
    return render_template("Admin/complaintreply.html")


@app.route("/display_complaint", methods=['post'])
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
def view_hospital():
    return render_template("Admin/hospital_view.html")

@app.route("/viewNurse")
def view_nurse():
    return render_template("Admin/nurse_view.html")

@app.route("/nurseHome")
def nurse_home():
    return render_template("Nurse/nursehome.html")

@app.route("/regNurse")
def reg_nurse():
    return render_template("Nurse/nursereg.html")

@app.route("/jobApply")
def job_apply():
    return render_template("Nurse/apply_job.html")

@app.route("/jobStatus")
def job_status():
    return render_template("Nurse/job_status.html")

@app.route("/addComplaintsNurse")
def add_complaints_nurse():
    return render_template("Nurse/complaints.html")

@app.route("/viewComplaintsNurse")
def view_complaints_nurse():
    return render_template("Nurse/view_complaints.html")



@app.route("/hospitalHome")
def hospital_home():
    return render_template("Hospital/hospitalhome.html")

@app.route("/regHospital")
def reg_hospital():
    return render_template("Hospital/hospitalreg.html")

@app.route("/addJob")
def add_job():
    return render_template("Hospital/add_job.html")

@app.route("/manageJob")
def manage_job():
    return render_template("Hospital/manage_job.html")

@app.route("/addComplaintsHospital")
def add_complaints_hospital():
    return render_template("Hospital/complaints.html")

@app.route("/viewComplaintsHospital")
def view_complaints_hospital():
    return render_template("Hospital/view_complaint.html")

if __name__ == "__main__":
    app.run(debug=True)

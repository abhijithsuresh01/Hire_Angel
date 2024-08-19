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
    resume.save("static/uploads", resume_name)

    qry="INSERT INTO `login` VALUES (NULL, %s, %s,`nurse`)"
    val=(username,password)
    id=iud(qry, val)

    qry="INSERT INTO `nurses` VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(id,fname,lname,phone,email,nurseid,speciality,experience,resume_name)

    iud(qry, val)

    return '''<script>alert("successfully registered");window.location="/"</script>'''

@app.route("/hospital_registration")
def hospital_reg() :
    return render_template("hospitalreg.html")




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

@app.route("/viewComplaint")
def view_complaint():
    return render_template("Admin/complaint.html")

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

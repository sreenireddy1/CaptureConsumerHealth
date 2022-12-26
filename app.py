from flask import Flask,flash,request,render_template,redirect,url_for
from pymongo import MongoClient
from Predict_Disease import NaiveBayes
from Doctor_Details import main
from Direct_Doctor_Details import Book_Appointment
config={
    "DEBUG":True 
}
app = Flask(__name__, static_url_path='/static')
app.secret_key = "abc"  

app.config.from_mapping(config)
client = MongoClient('localhost', 27017,serverSelectionTimeoutMS=4000)

db=client.capturehealth

@app.route('/')
def index():
    print("hello Capture health")
    return render_template("index.html")

@app.route('/loginform',methods=["GET","POST"])
def login():
    print("hello from login page")
    return render_template("login.html")

@app.route('/logindata',methods=["GET","POST"])
def logindata():
    logdata={}
    if request.method=="POST":
        logdata['logemail']=request.form['logemail']
        logdata['logpass']=request.form['logpass']

        #db.logindata.insert_one(logdata)
        #to get registration data and verify details
        x=db.registrationdata.find_one({ "logemail": logdata['logemail'],"logpass":logdata['logpass'] })
     
        if x:
            print(x)
            flash("You have logged in successfully ")
            return redirect("/quicksurvey")
        else:
            print("Details not found")
            flash("Details not found !!",'error')
            return redirect("/loginform")
    return redirect("/")

@app.route('/regdata',methods=["GET","POST"])
def regdata():
    regdata={}
    if request.method=="POST":
        regdata['logemail']=request.form['logemail']
        regdata['logpass']=request.form['logpass']
        regdata['clogpass']=request.form['c_logpass']
        regdata['logname']=request.form['logname']
        regdata['age']=request.form['age']
        regdata['phone']=request.form['phone']

        db.registrationdata.insert_one(regdata)

        #return redirect("/loglist")

    return redirect("/loginform")

@app.route('/appointment',methods=["GET","POST"])
def book_appointment():
    appointmentData={}
    if request.method=="POST":
        print("Appointment booking")
        appointmentData['patient_name']=request.form['patient_name']
        appointmentData['age']=request.form['u_age']
        appointmentData['phno']=request.form['u_phno']
        appointmentData['gender']=request.form['u_gender']
        appointmentData['email']=request.form['u_email']
        appointmentData['location']=request.form['u_location']
        appointmentData['disease']=request.form['Disease']
        #print(appointmentData['disease'])
        doctor=Book_Appointment(appointmentData['disease'])
        #print("from book appointment",doctor)
        appointmentData['doctor']=doctor
        appointmentData['date']=request.form['u_date']

        db.AppointmentData.insert_one(appointmentData)
        return render_template('appointment.html',doctor=doctor)

@app.route("/predicted/<disease>/<doctor>",methods=["GET","POST"])    
def predicted(disease,doctor):    
    if request.method=="POST":
        return render_template('predicted.html',disease_pred=disease,doctor=doctor,flag=1)
    else:
        return render_template('predicted.html',disease_pred=disease,doctor=doctor,flag=0)  

@app.route('/quicksurvey',methods=["GET","POST"])
def surveyform():
    return render_template('trail.html')
      
@app.route("/surveydata",methods=["GET","POST"])
def surveyfunc():
    surveydata={}
    consultData={}
    if request.method=="POST":
        if request.form["Submitt"]=="Predict":
            print("Predict")
            surveydata['user_name']=request.form['user_name']
            surveydata['Address']=request.form['Address']
            surveydata['user_email']=request.form['user_email']
            surveydata['phno']=request.form['number']
            surveydata['location']=request.form['location']
            surveydata['gender']=request.form['gender']
            surveydata['age']=request.form['age']
            surveydata['symptom1']=request.form['symptom1']
            surveydata['symptom2']=request.form['symptom2']
            surveydata['symptom3']=request.form['symptom3']
            surveydata['symptom4']=request.form['symptom4']
            surveydata['symptom5']=request.form['symptom5']
            surveydata['othersymp']=request.form['othersymp']

            surveydata['days']=request.form['days']
            diseasep=NaiveBayes(surveydata['symptom1'],surveydata['symptom2'],surveydata['symptom3'],surveydata['symptom4'],surveydata['symptom5'])
            print("disease",diseasep)
            surveydata['disease']=diseasep
            db.surveyData.insert_one(surveydata)

            #consultData['disease']=diseasep
            consultData={}
            print("consult")
            doctor=main()
            print("from app",doctor)
            #consultData['disease']=disease
            consultData['patient']=surveydata['user_name']
            consultData['disease']=diseasep
            consultData['doctor']=doctor
            db.ConsultData.insert_one(consultData)

            return redirect(url_for("predicted",disease=diseasep,doctor=doctor))

    return redirect("/quicksurvey")

@app.route("/loglist")    
def loglists():    
    #Display the all Tasks   
    x=db.logindata.find()
    print("list print",x)
    a1="active"    
    return render_template('results.html',students=x)  

@app.route("/consult/<doctor>")    
def consult(doctor):    
    #Display the all Tasks   
    x=db.surveyData.find()
    print("list print",x) 
    lastobject=db.surveyData.find().sort('_id',-1).limit(1);
    print(lastobject,"from surveylist")
    return render_template('predicted.html',doctor=doctor)

if __name__=="__main__":

    app.run(port=5000)


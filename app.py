## ALL INSIDE VIRTUAL ENVIRONMENT
# pip install flask

from flask import Flask, render_template, request,redirect, session, flash, Response
from flask_mail import Mail, Message
from pymongo import message
from core import book_activity, choose_resource, delete_activity, delete_booking, download_patient_data, get_activity, get_available_activities, get_stats, message_wrapper, register_user, update_activity, update_user, user_authenticate,find_stress_level
from core import  get_user_data,  get_resource, create_activity, inject_token, update_doc_suggestion, delete_doc_suggestion, create_doc_suggestion
from core import update_resource, delete_resource, create_resource, get_booked_activities, get_doc_suggestion, get_password
import random as ra
app = Flask(__name__)

app.secret_key="asude"

"""
    This works i have tested it. Just need to provide some email and test
"""
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'happymeinfinity0@gmail.com'
app.config['MAIL_PASSWORD'] = 'Happy@92'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)




@app.route("/")
def index():
    return render_template("index.html")


@app.route("/registration", methods=['GET', 'POST'])
def register():
    if request.method=="GET":
        return render_template("user_registration.html")
    else:
        resp=register_user(request)
        if resp['error'] is None:
            msg = Message(
                            resp['subject'],
                            sender ='arunangshu.biswas17@gmail.com',
                            recipients = resp['rec']
                        )
            msg.html = message_wrapper(resp['message'])
            mail.send(msg)
            flash('Congratulations! you are now a part of Happy me. ', 'success')
            return redirect("authentication")
        else:
            flash(resp['message'],'error')
            return redirect("/registration")
        


@app.route("/authentication", methods=['GET', 'POST'])
def authenticate():
    if request.method=="GET":
        return render_template("user_login.html")
    else:
        email=request.form['email']
        password=request.form['password']
        
        # user=User.query.filter_by(email=email).filter_by(password=password).first()
        user=user_authenticate(email, password)
        if user is None:
            flash("Invalid username or password!", 'error')
            return redirect('authentication')
        else:
            
            session['user_id']=str(user['_id'])
            session['user_email']=user['email']
            session['user_name']=user['name']
            session['stress']=user['stress']
            flash(f"Welcome {session['user_name']}", 'white-heading')
            return redirect('dashboard')



@app.route("/logout")
def logout():
    if session.get("admin") :
        session.clear()
        return redirect("adminAuth")
    else:
        session.clear()
        return redirect("authentication")


@app.route("/dashboard")
def dashboard():
    if(session.get("user_id")):
        # print(session.get("user_id"))
        # from core import test
        # test()
        return render_template("user_dashboard.html")
    else:
        return redirect("authentication")



@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    if request.method=='GET':
        return render_template("forgotpassword.html")
    else:
        email=request.form['email']
        
        user=get_password(email)
        rec=[]
        mail_message="Your old password is :"+user['password']+". Please log in and change the password in your profile section."
        user_email=user['email']
        print(user_email)
        rec.append(user_email)
        msg = Message(
                        'Ahoy! here is your old password',
                        sender ='happymeinfinity0@gmail.com',
                        recipients = rec
                    )
        msg.html = message_wrapper(mail_message)
        mail.send(msg)
        flash("A mail has been sent to the registered email address. In case you don't see any email in your inbox from happmeinfinity check your spam section.", 'success')
        return redirect('authentication')

@app.route("/info")
def info():
    return render_template("info.html")
    

@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method=="POST":
        message=request.form['message']
        email=request.form['email']
        name=request.form['name']   
        if(message=="" or email == "" or name==""):
            flash("Empty Fields ", "error")
            return redirect("/contact")
        msg = Message(
                        'A visitor has something to say',
                        sender ='happymeinfinity0@gmai.com',
                        recipients = ["happymeinfinity0@gmail.com"]
                    )
        msg.html = f"<h3>Name : {name} </h3><p>Email : {email}</p><hr><p>Message : {message}</p>"+message_wrapper("")
        mail.send(msg)
        flash("Your message has been sent to admin", 'success')
        return redirect("/contact")
    else:

        return render_template("contactus.html")

@app.route("/about")
def about():
    return render_template("aboutus.html")

@app.route("/survey", methods=[ 'POST'])
def track_stress():
    if request.method=="POST":
        resp=find_stress_level(request.form)
        if resp:
            return redirect("dashboard")
        else:
            return redirect("/error")

@app.route("/activity")
def activity():
    return render_template("activity.html")

@app.route('/funzone', methods=['GET', 'POST'])
def funzone():
    if(session.get('user_id')):
        if session.get('user_id') !="1admin1":
            games=('a', 'b', 'c', 'd')
            game=ra.choice(games)
            resource=choose_resource()
            resource["game"]=game
            return render_template("funzone.html",resource=resource)
        else:
            flash("Login as normal user", "error")
            return redirect("/authentication")    
    else:
        flash("Login first buddy !", "error")
        return redirect("/authentication")

@app.route("/userprofile", methods=["GET", "POST"])
def user_profile():
    if session.get("user_id"):
        if session.get("user_id")!="1admin1":
            if request.method=="GET":
                args=[]
                args.append(session.get("user_id"))
                args=args + ["name","dob", "contact", "aadhar", "address", "gender", "email"]
                # print(args)
                data=get_user_data(args)
                return render_template("user_profile.html", data=data)
            else:
                update_user(request.form)
                flash("user details updated successfully", "success")
                return redirect("/userprofile")
        else:
            flash("currently admin has no right to update profile", "error")
            return redirect("/authentication")    
    else:
        flash("Please login to access your profile", "error")
        return redirect("/authentication")

@app.route("/eventRegistration", methods=['GET', 'POST'])
def user_event_registraton():
    if request.method=="GET":
        if request.args.get("token") and request.args.get("id") and request.args.get("actId") and request.args.get("age") :
            u=get_user_data([request.args.get("id"), "token"])
            if u['token']==request.args.get("token"):
                inject_token("0", request.args.get("id"))
                info={
                    "user_id":request.args.get("id"),
                    "user_age":request.args.get("age"),
                    "activity_id":request.args.get("actId")
                }
                resp=book_activity(info)
                flash(resp['message'], "info")
            else:
                print("not safe to book")
                flash("invalid token", "info")
            return redirect("/eventRegistration")
        if session.get("user_id") != None:
            # with login case
            id=session.get("user_id")
            # print(id)
            if id=="1admin1":
                data=get_user_data([0, "_id"])
                return render_template("user_event_registration.html", ids=data)
            dic={"user_id":id}
            data=get_available_activities(dic)
            return render_template("user_event_registration.html",data=data)
        else:
            # without login case 
            data=get_user_data([0, "_id"])
            print("no user is logged in ")
            return render_template("user_event_registration.html", ids=data)
    
    else:
        # print(request.form)
        user_id=request.form['user_id']
        activity_id=request.form['activity_id']
        user_age=request.form['user_age']
        if user_id!=session.get("user_id"):
            #send confirmation email
            token=ra.randint(192817461, 906947362)
            user_email=inject_token(token, user_id)
            msg = Message(
                            'Event Booking confirmation',
                            sender ='happymeinfinity0@gmai.com',
                            recipients = [user_email]
                        )
            msg.html = f"<a href='{request.root_url}eventRegistration?token={token}&id={user_id}&actId={activity_id}&age={user_age}'>confirm event booking</a>"+message_wrapper("")
            mail.send(msg)
            flash("A confirmation booking email has been sent to your mail. ", "success")
            return redirect("/eventRegistration")
        else:
            resp=book_activity(request.form)       
            flash(resp['message'], "success")
        return redirect("/eventRegistration")

@app.route("/cancelBooking", methods=['GET'])
def cancel_booking():
    if session.get("user_id"):
        _id=request.args.get("id")
        print("Deleteing booking ")
        delete_booking({"_id":_id})
        flash("Booking cancelled successfully", "success")
        return redirect("/viewScheduledActivity")

@app.route("/viewScheduledActivity")
def view_scheduled_activity():
    if request.method=="GET":
        data=get_booked_activities()
        # print(data)
        return render_template("user_activity_scheduled.html", bookings=data)


@app.route("/doc-suggestion", methods=['GET', 'POST'])
def doc_suggestion():
    if session.get("user_id") and session.get("user_id")!="1admin1":
        docsuggestions=get_doc_suggestion()
        docsuggestion=ra.choice(docsuggestions)
        return render_template("user_view_doc_suggestion.html", docsuggestion=docsuggestion)
    else:
        flash("Login please", "error")
        return redirect("/authentication")


@app.route("/request-appointment", methods=['GET'])
def appointment_request():
    if session.get("user_id") and session.get("user_id")!="1admin1":
        
        mail_message=f"<h2>Dear admin</h2>,<br> <p> {session.get('user_name')} wants to book an appointment with a doctor</p> <hr> USER ID : {session.get('user_id')}<br> USER EMAIL : {session.get('user_email')}"
    
        msg = Message(
                        'Appointment request',
                        sender =session.get("user_email"),
                        recipients = ['happymeinfinity0@gmail.com']
                    )
        msg.html = message_wrapper(mail_message)
        mail.send(msg)

        mail_message=f"<h2>Dear admin</h2>,<br> <p> {session.get('user_name')} wants to book an appointment with a doctor</p> <hr> USER ID : {session.get('user_id')}<br> USER EMAIL : {session.get('user_email')}"
    
        msg = Message(
                        'Appointment request received.',
                        sender ="happymeinfinity0@gmail.com",
                        recipients = [session.get("user_email")]
                    )
        msg.html = f"<h3>Dear {session.get('user_name')} ,</h3><p>We have received your appointment request. Please be patient. In case of emergency please contatc on +91 9152487635 or +91 9635417265 or visit our hospital address </p><br> "+message_wrapper("")
        mail.send(msg)
        flash("You have successfully requested for an appointment ", "success")
        return redirect("/doc-suggestion")






@app.route('/userDetails', methods=['POST'])
def user_details():
    if request.method=="POST":
        params=request.get_json()
        user_details=get_user_data(params['query'])
        uid={}
        uid['user_id']=params['query'][0]
        user_activities=get_available_activities(uid)
        data={}
        data['user_details']=user_details
        data['available_activities']=user_activities
    return data
    
@app.route("/adminAuth", methods=['GET', 'POST'])
def admin_auth():
    if request.method=="GET":
        return render_template("admin_login.html")
    else:
        email=request.form['email']
        password=request.form['password']
        user=user_authenticate(email, password)
        if user is not None:
            session['user_id']=str(user['_id'])
            
            if(user['_id']=="1admin1"):
                session['admin']=True
                session['user_email']=user['email']
                session['user_name']=user['name']
                flash(f"Welcome {session['user_name']}", 'white-heading')
                return redirect('adminDashboard')
            else:
                flash("you are registered as normal user. Please log in via user login page", "success")
                return redirect("authentication")
        else:
            flash("No user found as per the credential provided ", "error")
            return redirect("adminAuth")

@app.route("/adminDashboard")
def admin_dashboard():
    if session.get("admin") :
        return render_template("admin_dashboard.html")
    else:
        return redirect("adminAuth")



@app.route("/manageActivities", methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_Activities():
    if request.method=="GET":
        data=get_activity()
        return render_template("admin_manage_activities.html", activities=data)
    elif request.method=="POST":
        print(request.form)
        resp=create_activity(request.form)
        flash(resp['message'], 'info')
        return redirect("/createOrUpdateActivity")
    elif request.method=="PUT":
        req=request.get_json()
        resp=update_activity(req)
        return resp
    elif request.method=="DELETE":
        req=request.get_json()
        resp=delete_activity(req)
        return resp
    
@app.route("/createOrUpdateActivity", methods=['GET', 'POST'])
def create_or_update_activity():
    if not session.get("admin"):
        return redirect("/adminAuth")
    if request.method=="GET":
        if ( request.args.get("id") is not None):
            data=get_activity(request.args.get("id"))

            return render_template("admin_create_or_update_activity.html", activity=data)
        else:
            return render_template("admin_create_or_update_activity.html")
    

@app.route("/assignActivity", methods=['GET', 'POST'])
def assign_activity():
    if session.get("user_id") != None:
        if session.get("user_id")=="1admin1":
            if request.method=="GET":
                if request.args.get("uid") is None:
                    user_data=get_user_data([0, "_id"])
                    return render_template("admin_assign_activity.html", userData=user_data)
                else :
                    available_activities=get_available_activities({"user_id":request.args.get("uid")})
                    user_info={}
                    user_info=get_user_data([request.args.get("uid"), "age", "name"])
                    booked_activities=get_booked_activities(request.args.get("uid"))
                    

                    user_info['booked_activities']=booked_activities
                    return {"available_activities":available_activities, "user_info":user_info}

            else:
                info=request.form
                resp=book_activity(info)
                if resp['code']==200:
                    flash("Activity has been assigned", "success")
                else:
                    flash(resp['message'], "error")
                return redirect("/assignActivity")
        else:
            flash("Admin priviledge is required", "error")
            return redirect("/adminAuth")
    else:
        flash("Admin priviledge is required", "error")
        return redirect("/adminAuth")


@app.route("/manageFunzone", methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_funzone():
    if not session.get("admin"):
        return redirect("/adminAuth")
    if request.method=="GET":
        # data=getFunzoneData()
        data=get_resource()
        return render_template("admin_manage_funzone.html", data=data)
    elif request.method=="PUT":
        req=request.get_json()
        print(req)
        data=update_resource(req)
        return data
    elif request.method=="POST":
        req=request.get_json()
        print(req)
        data=create_resource(req)
        return data
    elif request.method=="DELETE":
        req=request.get_json()
        print(req)
        data=delete_resource(req)
        return data

@app.route("/createOrUpdateResource", methods=['GET', 'POST'])
def create_or_update_resource():
    if not session.get("admin"):
        return redirect("/adminAuth")
    if request.method=="GET":
        if ( request.args.get("id") is not None):
            data=get_resource(request.args.get("id"))
            return render_template("admin_create_or_update_resource.html", resource=data)
        else:
            return render_template("admin_create_or_update_resource.html")
    

@app.route("/reports", methods=["GET", "POST"])
def generate_reports():
    if session.get("user_id")!="1admin1":
        flash("Admin priviledge is required")
        redirect("/adminAuth")
    else:
        if request.method=='GET' :
            typ=request.args.get("type")
            if typ=="patient":
                print("inside type=patient")
                st=request.args.get("st")
                sp=request.args.get("sp")
                gender=request.args.get("gender")
                if(sp and st):
                    if request.args.get("query")=="table":
                        frm=int(st)
                        to=int(sp)
                        
                        # print(f"{frm} {to}")
                        udet=get_user_data([0, "name", "stress", "contact", "address", "gender", "dob"])
                        resp=[]
                        # print(udet)
                        for u in udet:
                            try:
                                if frm <= int(u['stress']) <=to :
                                    if gender=="all":
                                        resp.append(u)
                                    elif u['gender']==gender:
                                        resp.append(u)
                            except Exception as e:
                                continue
                        # patients={"patients":resp}
                        d={}
                        d['resp']=resp
                        d['request']={"frm":frm, "to":to, "gender":gender}
                        # print(d)
                        return render_template("admin_generate_reports.html", data=d)
                    elif request.args.get("query")=="csv":
                        print(f"{int(st)}  {int(sp)} {gender}")
                        csvfile=download_patient_data(st=int(st),sp=int(sp), gender=gender)
                        # return csvfile
                        # strcsv=str(csvfile)
                        return Response(
                            csvfile.to_csv(),
                            mimetype="text/csv",
                            headers={"Content-disposition":
                                    "attachment; filename=patient_report.csv"})

                else:
                    data={}
                    return render_template("admin_generate_reports.html", data=data)
            else:
                data={}
                return render_template("admin_generate_reports.html",data=data) 
        else:
            flash("invalid request", "error")
            return redirect("/reports")
                    

@app.route("/manageDocSuggestion", methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_doc_suggestion():
    if request.method=="GET":
        data=get_doc_suggestion()
        return render_template("admin_manage_doc_suggestion.html", docsuggestions=data)
    elif request.method=="POST":
        print(request.form)
        resp=create_doc_suggestion(request.form)
        flash(resp['message'], 'info')
        return redirect("/createOrUpdateDocSuggestion")
    elif request.method=="PUT":
        req=request.get_json()
        resp=update_doc_suggestion(req)
        return resp
    elif request.method=="DELETE":
        req=request.get_json()
        resp=delete_doc_suggestion(req)
        return resp
    
@app.route("/createOrUpdateDocSuggestion", methods=['GET', 'POST'])
def create_or_update_doc_suggestion():
    if not session.get("admin"):
        return redirect("/adminAuth")
    if request.method=="GET":
        if ( request.args.get("id") is not None):
            data=get_doc_suggestion(request.args.get("id"))
            return render_template("admin_create_or_update_doc_suggestion.html", docsuggestion=data)
        else:
            return render_template("admin_create_or_update_doc_suggestion.html")           

            
@app.route("/stats", methods=['POST'])
def stats():
    if session.get("user_id")=="1admin1":
        resp={}
        resp=get_stats()
        print(resp)
        return resp
    else:
        flash("Login as admin ", "error")
        return redirect("adminAuth")

if __name__=="__main__":
    app.run(debug=True, port=8000) 
    # PORT CAN BE CHANGED to 8000 or 5500 or anything else
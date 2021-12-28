from datetime import date, datetime
from itertools import count 
from bson.objectid import ObjectId
from flask import session
from pymongo import MongoClient, message
from analyser import predict_stress_level
import random as ra
import json
from bson.json_util import dumps
from pandas import json_normalize
import numpy 

# cluster = MongoClient("mongodb+srv://admin213:mongox12@cluster0.ypdmm.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
cluster = MongoClient("mongodb+srv://admin:admin92@cluster0.lafsm.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database=cluster['mongo_db']
user=database['user']
counter=database['counter']
activity=database['activity']
funzone=database['funzone']
doc_suggestion=database['doctor_suggestions']
activity_booking=database['activity_booking']

#new changes for once and better
patient=database['patient']
admin=database['admin']



#REFRACTORED
def createId():
    data=counter.find_one_and_update(
        {"name":"id"},
        {"$inc" :{"seq" :1} }
    )
    key=""
    if data['seq'] <1000 and data['seq']>=100:
        key="P0"+str(data['seq'])
    elif data['seq'] <100 and data['seq'] >=10:
        key="P00"+str(data['seq'])
    elif data['seq'] < 10:
        key="P000"+str(data['seq'])
    return key


#REFRACTORED
def register_user(request):
    mail_message=""
    errmsg=""
    resp={}    
    rec=[]
    flag=True
    try:
        fname=request.form['fname']
        lname=request.form['lname']
        email=request.form['email']
        password=request.form['password']
        rpassword=request.form['rpassword']
        if(password!=rpassword):
            flag=False
        
        aadhar=request.form['aadhar']
        if(len(aadhar)!=12):
            flag=False
        dob=request.form['dob']
        address=request.form['address']
        contact=request.form['contact']
        gender=request.form['gender']

        dobObject=datetime.strptime(dob, "%Y-%m-%d")

        if(len(contact)!=10):
            flag=False
        u=patient.find_one({"email":email})
        if u==None:
            user_id=str(createId())
            patient.insert_one({
                "_id":user_id+"",
                "name":fname+" "+lname,
                "email":email,
                "password":password,
                "aadhar":aadhar,
                "gender":gender,
                "address":address,
                "contact":contact,
                "stress":-1,
                "status":'inactive',
                "dob":dobObject
            })
            mail_message+=f"<h2>Welcome {fname} {lname}</h2>.<p> We are glad you joined us! Your USER_ID is {user_id}. Keep your password safe</p><hr>"
        else:
            flag=False
            errmsg="Uh Oh It seems that You have already registered by this email id. Incase you have forgot your password you can get back your old password in forgot password section."

        rec.append(email)
    except Exception as e:
        errmsg=str(e)
        flag=False
    
    if(flag):
        resp['subject']='Happy Me!'
        resp['message']=mail_message
        resp['rec']=rec
        resp['error']=None
        return resp
    else:
        resp['message']=errmsg
        resp['error']=True
        return resp


#REFRACTORED
def user_authenticate(email, password):
    u=patient.find_one({"email":email, "password":password})
    a=admin.find_one({"email":email, "password":password})

    if u:
        return u
    elif a :
        return a
    else:
        return None


#REFRACTORED
def find_stress_level(resp):
    answers=[]
    user_response=[]
    user_response.append(int(resp['happy']))
    user_response.append(int(resp['peopleMet']))
    user_response.append(int(resp['productive']))
    user_response.append(int(resp['positivity']))
    user_response.append(int(resp['sleep']))
    user_response.append(int(resp['social']))
    answers.append(user_response)

    stress_level=predict_stress_level(answers)
    # print(stress_level)
    try:
        patient.find_one_and_update({"_id" : str(session['user_id']) }, {"$set":{'stress':int(stress_level)} })
        session["stress"]=str(stress_level)
    except Exception as e:
        print(e)
    return True


#REFRACTORED 
def update_user(user_data):
    fname=user_data["fname"]
    lname=user_data["lname"]
    gender=user_data["gender"]
    dob=user_data["dob"]
    aadhar=user_data["aadhar"]
    address=user_data["address"]
    contact=user_data["contact"]
    email=user_data["email"]
    _id=session.get("user_id")
    name=fname+" "+lname
    u=None
    dobObject=datetime.strptime(dob, "%Y-%m-%d")
    try:
        if user_data['password']=='':
            u=patient.find_one_and_update({"_id":_id}, {"$set":{"name":name, "gender":gender, "dob":dobObject, "aadhar":aadhar, "address":address, "contact":contact, "email":email}})
        else:
            u=patient.find_one_and_update({"_id":_id}, {"$set":{"name":name, "gender":gender, "dob":dobObject, "aadhar":aadhar, "address":address, "contact":contact, "email":email, "password":user_data["password"]}})
    except Exception as e:
        print(e)
    return u 


#REFRACTORED
def get_user_data(param):
    """
        tok=param[0] is the id
        0 should be given to get all user details
        param[1-n] is the list of all the attributes which are compulsory
        attributes are : 
        id, name, email, password, aadhar, gender, address, contact, stress, status, dob
    """
    tok=param[0]
    if tok==0:
        # find all
        users=patient.find() 
        respList=[]
        for individual in users:
            resp={}
            for i in range(1,len(param)):
                
                resp[param[i]]=individual[param[i]]
            respList.append(resp)  
        # print(respList)  
        return respList
        # return 
    else:
        # find by id
        resp={}
        data=patient.find_one({"_id" : tok})
        for i in range(1,len(param)):
            if param[i]=="age":
                dob=data['dob']
                currentDate=datetime.now()
                td=currentDate-dob
                age=td.days//365
                resp['age']=age
            elif param[i]=="dob":
                resp[param[i]] = str(data[param[i]]).split(" ")[0]
            else:
                resp[param[i]]=data[param[i]]
        # print(resp)
        return resp



"""
/*-------------------------------------
*   FUNZONE
*/-------------------------------------
"""

#NO CHANGE
def get_resource(*args):
    resource={}
    if args==():
        resource=funzone.find()
    else:
        resource=funzone.find_one({"_id":ObjectId(args[0])})
    return resource


#NO CHANGE
def choose_resource():
    joke=ra.choice(list(funzone.find({"type":"joke"})))
    quote=ra.choice(list(funzone.find({"type":"quote"})))
    video=ra.choice(list(funzone.find({"type":"video"})))
    resource={}
    resource['joke']=joke
    resource['quote']=quote
    resource['video']=video
    return resource


#NO CHANGE
def update_resource(dic):
    _id=dic['id']
    _rc=dic['resource']
    _type=dic['type']
    code=0
    msg=""
    try:
        funzone.find_one_and_update({"_id":ObjectId(_id)}, {"$set":{'type':_type, "resource":_rc}})
        msg="updated successfully"
        code=200
    except Exception as e:
        print(e)
        msg=e
        code=400
    return {"message":msg, "code":code}


#NO CHANGE
def create_resource(dic):
    
    _rc=dic['resource']
    _type=dic['type']
    code=0
    msg=""
    try:
        funzone.insert_one({'type':_type, "resource":_rc})
        msg="resource added successfully"
        code=200
    except Exception as e:
        print(e)
        msg=e
        code=400
    return {"message":msg, "code":code}


#NO CHANGE
def delete_resource(dic):
    _id=dic['id']
    code=0
    msg=""
    try:
        funzone.find_one_and_delete({"_id":ObjectId(_id)})
        msg="resource has been removed successfully"
        code=200
    except Exception as e:
        print(e)
        msg=e
        code=400
    return {"message":msg, "code":code}



"""
/*-------------------------------------
*   doc_suggestion
*/-------------------------------------
"""



#NO CHANGE
def get_doc_suggestion(*args):
    print(args)
    if args==():
        lst_doc_suggestion=list(doc_suggestion.find())
        return lst_doc_suggestion
    else:
        docsuggestion=doc_suggestion.find_one({'_id':ObjectId(args[0])})
        return docsuggestion


#NO CHANGE
def create_doc_suggestion(form):
    doc_says=form['doc_says']
    code=0
    message=""
    stress=form['stress']
    try :
        doc_suggestion.insert_one({"doc_says":doc_says, "stress":int(stress)})
        message="suggestion created"
    except Exception as e:
        print(e)
        code=400
        message=e
    resp={"message":message, "code":code}
    return resp


#NO CHANGE
def delete_doc_suggestion(dic):
    _id=dic['_id']
    code=0
    msg=""
    try:
        doc_suggestion.find_one_and_delete({"_id":ObjectId(_id)})
        msg="doc_suggestion has been removed successfully "
        code=200
    except Exception as e:
        print(e)
        msg=e
        code=400
    return {"message":msg, "code":code}


#NO CHANGE
def update_doc_suggestion(dic):
    _id=dic['_id']
    _doc_says=dic['doc_says']
    _stress=dic['stress']
    code=0
    msg=""
    try:
        doc_suggestion.find_one_and_update({"_id":ObjectId(_id)}, {"$set":{'doc_says':_doc_says, "stress":_stress}})
        msg="updated successfully"
        code=200
    except Exception as e:
        print(e)
        msg=e
        code=400
    return {"message":msg, "code":code}




"""
/*-------------------------------------
*   FORGOT PASSWORD
*/-------------------------------------
"""


#REFRACTORED
def get_password(email):
    u=patient.find_one({"email":email})
    a=admin.find_one({"email":email})
    if u:
        return u
    elif a:
        return a
    else:
        return None



"""
/*-------------------------------------
*   USER STATS
*/-------------------------------------
"""



#REFRACTORED 
def get_stats():
    temp=patient.find({})
    list_of_lists=[['stress_category', 'level' ]]
    low=0
    medium=0
    high=0
    count=0
    # print(list(temp))
    for data in temp:
        if data.get("stress"):
            count+=1
            if  1 <= data.get("stress") <=2:
                low+=1
            elif 3 <= data.get("stress") <=4:
                medium+=1
            elif 5<= data.get("stress") < 6:
                high+=1
    list_of_lists.append(["low",low ])
    list_of_lists.append(["medium", medium ])
    list_of_lists.append(["high",high ])
    resp={}
    resp['arrayInfo']=list_of_lists
    resp['total']=count
    return resp





"""
/*-------------------------------------
*   ACTIVITY
*/-------------------------------------
"""



#REFRACTORED
def create_activity(form):
    status="scheduled"
    message=""
    resp={}    
    start=form['start']
    end=form['end']

    st=datetime.strptime(start, '%Y-%m-%dT%H:%M')
    en=datetime.strptime(end, '%Y-%m-%dT%H:%M')
    diff=int((en-st).total_seconds()//3600)
    if(diff<=0 or st<datetime.now()):
        message+="Invalid duration"
        resp['message']=message
        resp['status']=False
        return resp
    else:

        data={ "a_name":form['a_name'],
                "start_time":st,
                "end_time":en,
                "summary":form['summary'],
                "venue":form['venue'],
                "status":status
            }
        activity.insert_one(data)
        resp['message']="Activity created"
        resp['status']=True
        return resp


#NO CHANGE
def get_activity(*args):
    data={}
    if args==():
        data=activity.find()
    else:
        data=activity.find_one({"_id":ObjectId(args[0])})
    return data



#NO CHANGE
def delete_activity(dic):
    _id=dic['_id']
    code=0
    msg=""
    try:
        activity.find_one_and_delete({"_id":ObjectId(_id)})
        # check this activity in activity booking 
        activity_booking.delete_many({"activity_id":_id})
        msg="Activity has been removed successfully also its corresponding booking has been deleted"
        code=200
    except Exception as e:
        print(e)
        msg=e
        code=400
    return {"message":msg, "code":code}



#REFRACTORED
def update_activity(dic):
    _id=dic['_id']
    _aname=dic['a_name']
    _start=dic['start']
    _st=datetime.strptime(_start, "%Y-%m-%dT%H:%M")
    _end=dic['end']
    _en=datetime.strptime(_end, "%Y-%m-%dT%H:%M")
    _summary=dic['summary']
    _venue=dic['venue']
    _status=dic['status']
    code=0
    msg=""
    try:
        activity.find_one_and_update({"_id":ObjectId(_id)}, {"$set":{'a_name':_aname, "start_time":_st, "end_time":_en, "summary":_summary,"venue":_venue, "status": _status}})
        if _status=="closed":
            print("deleting closed activity from booking ")
            activity_booking.delete_many({"activity_id":_id})
        
        msg="Updated successfully"
        code=200
    except Exception as e:
        print(e)
        msg=e
        code=400
    return {"message":msg, "code":code}



#REFRACTORED
def get_available_activities(data):
    """
        input: {"user_id":id}
        output: activity details which user haven't registered for 
    """
    user_id=data['user_id']
    try:
            
        booked_activities=activity_booking.find({"user_id":user_id})
        booked_activity_ids=[]
        for act in booked_activities:
            booked_activity_ids.append(ObjectId(act["activity_id"]))
        # print(f"{booked_activity_ids}")

        activities=activity.find({"_id":{"$nin":booked_activity_ids}})

        list_of_activities=[]
        for act in activities:
            a={}
            a['_id']=str(act["_id"])
            a['a_name']=act["a_name"]
            a['start']=act['start_time']    
            a['end']=act['end_time'] 
            

            a['summary']=act['summary']
            a['venue']=act['venue']
            if(a['start']>=datetime.now() and act['status'] != "closed" ):
                list_of_activities.append(a)
        # print(list_of_activities)
        return list_of_activities
    except Exception as e:
        print(e)
    return None

    

#NO CHANGE
def book_activity(info):
    """
    input: info - dictionary
        info['admin_msg']
        activity_id=info['activity_id']
        user_id=info['user_id']
        user_age=info['user_age']
    """
    message=""
    code=0
    try:
        activity_id=info['activity_id']
        user_id=info['user_id']
        user_age=info['user_age']
        if(activity_id=="None" or user_id == "None" or user_age == "None"):
            message="Invalid data received"    
            code=200
        else:
            admin_msg=""
            if info.get("admin_msg"):
                admin_msg=info["admin_msg"]
            else:
                admin_msg=""
            activity_booking.insert_one({"activity_id":activity_id, "user_id":user_id, "user_age":user_age,"admin_msg":admin_msg})
            message="Congratulations activity has been booked successfully."
            code=200
    except Exception as e :
        message=e
        code=400
    return {"message":message, "code":code}



#REFRACTORED    
def get_booked_activities(*args):  
    """
        input: You can either pass a tuple with only one parameter as id
        or call the function directly to fetch booked activities with the help of user_id stored in session
    """
    resp={}
    try:
        _id=session.get("user_id")
        if args!=():
            _id=args[0]
        # print(args)
        bookings=activity_booking.find({"user_id":_id})
        lst=[]
        if bookings:
            for booking in bookings:
                instance={}
                instance['activity']=activity.find_one({"_id":ObjectId(booking["activity_id"])})
                print("this is date --> ",instance["activity"]['start_time'])
                st=instance["activity"]['start_time']
                en=instance["activity"]['end_time']
                
                current_status=""
                if st < datetime.now() < en:
                    current_status="on-going"
                    # print(f"{booking['a_name']} | {sch}")
                elif datetime.now() <st:
                    current_status="scheduled"
                    # print(f"{booking['a_name']} | {sch}")
                elif en < datetime.now():
                    current_status="complete"
                    # print(f"{booking['a_name']} | {sch}")
                print(current_status)
                instance['activity']['start_time']=st.strftime("%Y-%m-%dT%H:%M")
                instance['activity']['end_time']=en.strftime("%Y-%m-%dT%H:%M")
                instance['activity']=json.loads(dumps( instance['activity']))
                instance['current_status']=current_status
                instance['admin_msg']=booking['admin_msg']
                instance['_id']=str(booking['_id'])
                # print(instance['activity'])
                lst.append(instance)
            resp['bookings']=lst    
        else:
            resp['bookings']=None
            resp['code']=200
            resp['msg']="No bookings found"
        # print(resp)
    except Exception as e:
        print(e)
        resp['msg']=str(e)
        resp['bookings']=None
        resp['code']=400
        print(resp)
    return resp
    


#REFRACTORED
def download_patient_data(**kargs):
    """
        kargs : stress minimum, stress maximum
        st=val1, sp=val2
    """
    document=None
    st=kargs.get("st")
    sp=kargs.get("sp")
    gender=kargs.get("gender")
    print(f"{st} {sp} {gender}")
    if gender=="all":
        document = patient.find({"stress":{"$gte":st, "$lte":sp}})
    else:
        document = patient.find({
            "stress": {"$gte":st,  "$lte":sp},
            "gender": {"$eq":gender}
    })
    # print(list(document))

    json_string = dumps(document)
    print(json_string)
    json_obj = json.loads(json_string)
    
    data1 = json_normalize(json_obj)
    # x=data1.to_string(header=True,
    #               index=False,
    #               index_names=False).split('\n')
    # print(x)
    
    # # print(str(data1))
    print(type (data1))
    return data1






















def delete_booking(dic):
    _id=dic["_id"]
    activity_booking.delete_one({"_id":ObjectId(_id)})
    return True







def inject_token(token, user_id):
    u=patient.find_one_and_update({"_id":user_id}, {"$set":{"token":str(token)}})
    return u['email']
    # print(str(token)+" "+user_id)

    

    
















def message_wrapper(m):
    m+="<br>Thank you <p>Team Happy me</p> "
    return m

# if __name__=="__main__":
#     dt="2021-12-24T13:26"
#     st=datetime.strptime(dt, '%Y-%m-%dT%H:%M')
#     tp=datetime.timestamp(st)
#     print(tp)
#     ndt=datetime.fromtimestamp(tp)
#     p=database['patient']
#     p.insert_one({"name":"Arunangshu Biswas",
#         "dob": st,
#         "gender":True
#     })

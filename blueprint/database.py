import pyrebase
import requests
import hashlib
import json
from datetime import date
import random
import string

config = {
	'apiKey': "AIzaSyB3EuVdoM4dHQCUwEYScbvbnxiXGXObdnc",
	'authDomain': "fyp-22-s3-07.firebaseapp.com",
	'projectId': "fyp-22-s3-07",
	'storageBucket': "fyp-22-s3-07.appspot.com",
	'messagingSenderId': "787854218747",
	'appId': "1:787854218747:web:85731507643d24aa3e275e",
	'measurementId': "G-R5DHSG3RTK",
	'databaseURL':''

}

databaseconfig = {
"apiKey": "AIzaSyB3EuVdoM4dHQCUwEYScbvbnxiXGXObdnc",
"authDomain": "fyp-22-s3-07.firebaseapp.com",
"databaseURL": "https://fyp-22-s3-07-default-rtdb.asia-southeast1.firebasedatabase.app",
"projectId": "fyp-22-s3-07",
"storageBucket": "fyp-22-s3-07.appspot.com",
"serviceAccount": "serviceAccountKey.json"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

firebase = pyrebase.initialize_app(databaseconfig)
database = firebase.database()
storage =firebase.storage()

def register_user(username,password):
    user = auth.create_user_with_email_and_password(username,password)
    #auth.send_email_verification(user['idToken'])

def set_user_information(username,user_information):
    database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).set(user_information)

def update_user_information(username,user_information):
    database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).update(user_information)

def login_user(username,password):
    user = auth.sign_in_with_email_and_password(username,password)
    user_information = get_general_user_information(username)
    return user,user_information

def get_general_user_information(username): #have a function that returns name, role dictionary object
    user = database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).get()
    name = user.val()["firstname"]+" " + user.val()["lastname"]
    role = user.val()["role"]
    return {"fullname":name,"role":role}

def firebase_user_information(user):
    return auth.get_account_info(user['idToken'])

def get_random_password(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def createDemoAccount():
    demo_username = get_random_password(8)+"@gmail.com"
    demo_password = get_random_password(8)
    user = auth.create_user_with_email_and_password(demo_username,demo_password)
    return demo_username,demo_password
    
def set_demo_user(username,user_information):
    user = database.child("demo_users").child(hashlib.sha256(username.encode()).hexdigest()).set(user_information)

def demo_user_exist(username):
    try:
        all_demo_users = database.child("demo_users").get()
        for user in all_demo_users.each():
            if username == user.val()['email']:
                return True
        return False
    except:
        return False
    
def get_demo_information(email):
    user = database.child("demo_users").child(hashlib.sha256(email.encode()).hexdigest()).get()
    name = user.val()["firstname"]+" " + user.val()["lastname"]
    demo_username = user.val()["demo_username"]
    demo_password = user.val()["demo_password"]
    return name,demo_username,demo_password

def get_faqs():
    all_faqs = database.child("faqs").get()
    faq_lists = []
    for user in all_faqs.each():
        faq_lists.append({"question":user.key(),"answer":user.val()})
    return faq_lists
   
def get_monthly_pricing():
    all_pricing = database.child("pricing").child("monthly").get()
    all_monthly_pricing_list = {}
    for user in all_pricing.each():
        all_monthly_pricing_list[user.key()] = user.val()
    return all_monthly_pricing_list

def get_yearly_pricing():
    all_pricing = database.child("pricing").child("yearly").get()
    all_yearly_pricing_list = {}
    for user in all_pricing.each():
        all_yearly_pricing_list[user.key()] = user.val()
    return all_yearly_pricing_list

def get_plan_pricing(amt):
    amount = int(amt)
    if amount <= 109:
        all_pricing = database.child("pricing").child("monthly").get()
        for plan in all_pricing.each():
            if plan.val() == amount:
                return {"plan": {"type" : "monthly", "desc":plan.key(),"cost":amount,"expiry":""}}
    else:
        all_pricing = database.child("pricing").child("yearly").get()
        for plan in all_pricing.each():
            if plan.val() == amount:
                return {"plan": {"type" : "monthly", "desc":plan.key(),"cost":amount,"expiry":""}}
                
def set_subscription(username,amount):#need to define for expiry, once approve the expiry will start?
    current_plan = get_plan_pricing(amount)
    database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).update(current_plan)
    
def retrieve_project_id(username):
    try:
        all_project = database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).child("projects").get()
        print(all_project)
        index = 0;
        for proj in all_project.each():
            index+=1
        return index
    except TypeError as e:
        return 1

def retrieve_all_project(username):
    try:
        all_project = database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).child("projects").get()
        all_project_list = []
        for proj in all_project.val():
            if proj != None:
                all_project_list.append({"id":proj["id"],"pname":proj["pname"],"category":proj["category"],"url":proj["url"]})
        return all_project_list
    except TypeError as e:
        return []
    
def set_project(username, project_information):
    database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child(project_information["id"]).update(project_information)
    
def delete_project_by_id(username, project_id):
    database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child(project_id).remove()

def get_project_by_id_exists(username,project_id):
    try:
        all_project = database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child(project_id).get()
        return all_project.val() != None
    except TypeError as e:
        return False
    
def get_store_owner_information(username):
    user = database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).get()
    name = user.val()["firstname"]+" " + user.val()["lastname"]
    fname = user.val()["firstname"]
    lname = user.val()["lastname"]
    cname = user.val()["company"]
    url = user.val()["url"]
    email = user.val()["username"]
    contact = user.val()["contact"]
    industry = user.val()["industry"]
    
    return {"fname":fname,"lname":lname, "name":name,"email":email,"url": url,"company": cname,"industry":industry,"contact":contact}
    
def get_project_by_id(username,project_id):
    try:
        all_project = database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child(project_id).get()
        if all_project.val() != None:
            return {"id":all_project.val()["id"],"pname":all_project.val()["pname"],"category":all_project.val()["category"],"url":all_project.val()["url"]}
        return None
    except TypeError as e:
        return None
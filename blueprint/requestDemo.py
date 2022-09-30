from flask import Blueprint,redirect, url_for,render_template,send_from_directory, request,session,flash
import pyrebase
import json
import requests
import hashlib
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

def get_random_password(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def createDemoUser(username):
    demo_username = get_random_password(8)+"@gmail.com"
    demo_password = get_random_password(8)
    try:
        user = auth.create_user_with_email_and_password(demo_username,demo_password)
        print(user)	
        info = auth.get_account_info(user['idToken'])
        print(info)	
    except requests.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
    return demo_username,demo_password

requestDemo = Blueprint('requestDemo', __name__, template_folder='templates')
@requestDemo.route("/demo", methods=["POST","GET"])
def request_demo():
    if request.method == "POST":
        username = request.form["email"]
        user_exist = False
        try:
            all_demo_users = database.child("demo_users").get()
            for user in all_demo_users.each():
                if username == user.val()['email']:
                    user_exist = True
                    print("user is already in demo")
                    flash("Email already exists, you already registered for demo!")      
                    return redirect("/demo")
                else:
                    user_exist = False
                    demo_username,demo_password = createDemoUser(username)
                    user_information= {"email":username,"phonenumber":request.form["phone_number"], "firstname":request.form["fname"],"lastname":request.form["lname"],"country":request.form["country"],"url":request.form["url"],"comment":request.form["comment"],"requesteddate":date.today().strftime("%d/%m/%Y"),"demo_username":demo_username,"demo_password":demo_password}
                    database.child("demo_users").child(hashlib.sha256(username.encode()).hexdigest()).set(user_information)
                    return redirect("/") 
        except requests.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            demo_username,demo_password = createDemoUser(username)
            user_information= {"email":username,"phonenumber":request.form["phone_number"], "firstname":request.form["fname"],"lastname":request.form["lname"],"country":request.form["country"],"url":request.form["url"],"comment":request.form["comment"],"requesteddate":date.today().strftime("%d/%m/%Y"),"demo_username":demo_username,"demo_password":demo_password}
            database.child("demo_users").child(hashlib.sha256(username.encode()).hexdigest()).set(user_information)
            return redirect("/") 
        #finally:    
            #if user_exist:
                #print("user is already in demo")
                #flash("Email already exists, you already registered for demo!")      
                #return redirect("/demo")
            #else:               
                #demo_username,demo_password = createDemoUser(username)
                #user_information= {"email":username,"phonenumber":request.form["phone_number"], "firstname":request.form["fname"],"lastname":request.form["lname"],"country":request.form["country"],"url":request.form["url"],"comment":request.form["comment"],"requesteddate":date.today().strftime("%d/%m/%Y"),"demo_username":demo_username,"demo_password":demo_password}
                #database.child("demo_users").child(hashlib.sha256(username.encode()).hexdigest()).set(user_information)
                #return redirect("/demo")        
    return render_template("request_demo.html")

@requestDemo.route("/faq")
def faq():
    all_faqs = database.child("faqs").get()
    faq_lists = []
    test = ""
    for user in all_faqs.each():
        faq_lists.append({"question":user.key(),"answer":user.val()})
    return render_template("faq.html",faq_lists=faq_lists)

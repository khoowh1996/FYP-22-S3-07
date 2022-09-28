from flask import Blueprint,redirect, url_for,render_template,send_from_directory, request,session,flash
import pyrebase
import json
import requests
import hashlib

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

requestDemo = Blueprint('requestDemo', __name__, template_folder='templates')
@requestDemo.route("/demo", methods=["POST","GET"])
def register():
	if request.method == "POST":
		#session.permanent = True
		username = request.form["email"]
		#password = request.form["password"]
		#print(request.form)
		#session["user"] = username
		#session["password"] = password
		#try:
		#	user = auth.create_user_with_email_and_password(username,password)
		#	print(user)	
		#	info = auth.get_account_info(user['idToken'])
		#	print(info)	
		#except requests.HTTPError as e:
		#	error_json = e.args[1]
		#	error = json.loads(error_json)['error']['message']
		#	if error == "EMAIL_EXISTS":
		#		print("Email already exists")
		#		flash("Email already exists")			
		#	elif error == "TOO_MANY_ATTEMPTS_TRY_LATER":
		#		print("You have attempted too many times...")
		#		flash("You have attempted too many times...")
		#	session.pop("user",None)
		#	session.pop("password",None)
		#finally:
		user_information= {"email":username,"phonenumber":request.form["phone_number"], "firstname":request.form["fname"],"lastname":request.form["lname"],"country":request.form["country"],"url":request.form["url"],"comment":request.form["comment"]}
		database.child("demo_users").child(hashlib.sha256(username.encode()).hexdigest()).set(user_information)
		return redirect("/")
		#if "user" in session:
		#	return redirect(url_for("authentication.user"))
	#if "user" in session:
	#	return redirect("/")
	return render_template("request_demo.html")

@requestDemo.route("/faq")
def faq():
    all_faqs = database.child("faqs").get()
    faq_lists = []
    test = ""
    for user in all_faqs.each():
        faq_lists.append({"question":user.key(),"answer":user.val()})
    return render_template("faq.html",faq_lists=faq_lists)

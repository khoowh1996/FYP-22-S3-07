from flask import Blueprint,redirect, url_for,render_template,send_from_directory, request,session,flash
import pyrebase
import json
import requests

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

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

authentication = Blueprint('authentication', __name__, template_folder='templates')
@authentication.route("/login", methods=["POST","GET"])
def login():
	if request.method == "POST":
		session.permanent = True
		username = request.form["username"]
		password = request.form["password"]
		print(request.form)
		session["user"] = username
		session["password"] = password
		try:
			user = auth.sign_in_with_email_and_password(username,password)
			print(user)	
			info = auth.get_account_info(user['idToken'])
			print(info)	
		except requests.HTTPError as e:
			error_json = e.args[1]
			error = json.loads(error_json)['error']['message']
			if error == "EMAIL_EXISTS":
				print("Email already exists")
				flash("Email already exists")
			elif error == "INVALID_PASSWORD":
				print("Invalid Password")
				flash("Invalid Password...")            
			elif error == "EMAIL_NOT_FOUND":
				print("Email not found")
				flash("Email does not exists")
			elif error == "TOO_MANY_ATTEMPTS_TRY_LATER":
				print("You have attempted too many times...")
				flash("You have attempted too many times...")
			session.pop("user",None)
			session.pop("password",None)
            
		#if user == None:
		#	return redirect(url_for("authentication.login"))
		#print(user)	
		#info = auth.get_account_info(user['idToken'])
		#print(info)			
		return redirect(url_for("authentication.user"))
		if "user" in session:
			return redirect(url_for("authentication.user"))
	if "user" in session:
		return redirect("/")
	return render_template("login.html")

@authentication.route("/logout")
def logout():
    session.pop("user",None)
    session.pop("password",None)
    return redirect(url_for("authentication.login"))

@authentication.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        password = session["password"]
        return f"<h1>{user}</h1><h1>{password}</h1>"
    return redirect(url_for("authentication.login"))


#email = 'test@gmail.com'
#password = '123456'

#user = auth.create_user_with_email_and_password(email,password)
#print(user)


#user = auth.sign_in_with_email_and_password(email,password)
#print(user)
#info = auth.get_account_info(user['idToken'])
#print(info)


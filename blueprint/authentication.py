from flask import Blueprint,redirect, url_for,render_template,send_from_directory, request,session,flash
import json
import requests
from blueprint.database import *

authentication = Blueprint('authentication', __name__, template_folder='templates')
@authentication.route("/login", methods=["POST","GET"])
def login():
	if request.method == "POST":
		session.permanent = True
		username = request.form["username"].lower()
		password = request.form["password"]
		session["user"] = username
		session["password"] = password
		try:
			user,user_information = login_user(username,password)
			print(user)
			print(firebase_user_information(user))
			if user_information != None:
				print(user_information)
				session["role"] = user_information["role"] 
				session["fullname"] = user_information["fullname"]
		except requests.HTTPError as e:
			error_json = e.args[1]
			error = json.loads(error_json)['error']['message']
			if error == "INVALID_PASSWORD":
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
			flash("Please try again, in a short while.")
			return redirect(url_for("authentication.login"))
		if "url" in session:
			curr_url = session["url"]
			session.pop("url",None)
			return redirect(curr_url)
		print(session["role"])
		if session["role"] == "demo_user":
			flash("Login Successfully!")
			return redirect("/projectoverview")
		if session["role"] == "store_owner":
			if get_status(username):
				flash("Login Successfully!")
				return redirect("/projectoverview")
			else:
				flash("Your account has been frozen, Please contact our Moderator at myrecommendservices@gmail.com.")
				return redirect("/logout")
		elif session["role"] == "moderator": 
			flash("Login Successfully!")
			return redirect("/moderatoroverview")
		elif session["role"] == "administrator":
			flash("Login Successfully!")
			return redirect("/administratoroverview")
		else:
			return redirect("/")
	if "user" in session:
		return redirect("/")
	return render_template("login.html")

@authentication.route("/logout")
def logout():
    session.pop("user",None)
    session.pop("password",None)
    session.pop("fullname",None)
    session.pop("role",None)
    flash("You have logged out successfully.")
    return redirect("/")
    #return redirect(url_for("authentication.login"))

@authentication.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        password = session["password"]
        role = session["role"]
        return f"<h1>{user}</h1><h1>{password}</h1><h1>{role}</h1>"
    return redirect(url_for("authentication.login"))

@authentication.route("/register", methods=["POST","GET"])
def register():
	if request.method == "POST":
		username = request.form["username"].lower()
		password = request.form["password"]
		try:
			user_information= {"username":username,"deleteid":get_encrypted_id(password,username), "firstname":request.form["fname"],"lastname":request.form["lname"],"company":request.form["cname"],"industry":request.form["industry"],"contact":request.form["contact"],"url":request.form["url"],"emailverification":False,"role":"sign_up_user","status":"pending"} #role = sign_up_user
			register_user(username,password)
			set_sign_up_user_information(username,user_information)			
			flash("Registration Success! Please login to your newly created account")
			return redirect(url_for("authentication.login"))
		except requests.HTTPError as e:
			error_json = e.args[1]
			error = json.loads(error_json)['error']['message']
			if error == "EMAIL_EXISTS":
				print("Email already exists")
				flash("Email already exists")			
			elif error == "TOO_MANY_ATTEMPTS_TRY_LATER":
				print("You have attempted too many times...")
				flash("You have attempted too many times...")
			return redirect(url_for("authentication.register"))	
	if "user" in session:
		return redirect("/")
	return render_template("register.html")

@authentication.route("/forgotpassword", methods=["POST","GET"])
def forgotpassword():
    if request.method=="POST":
        email = request.form["email"]
        try:
            reset_password(email)
            flash("reset email has been sent to your email.Please login to your email to reset your password.")
            return redirect("/login")
        except requests.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']         
            if error == "EMAIL_NOT_FOUND":
                print("Email not found")
                flash("Email does not exists")
            return redirect("/forgotpassword")
    return render_template("forgot_password.html")

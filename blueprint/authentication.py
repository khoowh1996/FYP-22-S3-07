from flask import Blueprint,redirect, url_for,render_template,send_from_directory, request,session,flash
import json
import requests
from blueprint.database import *

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
			#user = auth.sign_in_with_email_and_password(username,password)
			#print(user)	
			#info = auth.get_account_info(user['idToken'])
			#print(info)	
			user,user_information = login_user(username,password)
			print(user)
			print(firebase_user_information(user))
			session["role"] = user_information["role"] 
			session["fullname"] = user_information["fullname"] 
            flash("Login Successfully!")
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
		return redirect("/projectoverview")
		if "user" in session and session["role"] == "store_owner":
			return redirect("/projectoverview")
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
		#session.permanent = True
		username = request.form["username"]
		password = request.form["password"]
		print(request.form)
		#session["user"] = username
		#session["password"] = password
		try:
			#user = auth.create_user_with_email_and_password(username,password)
			#print(user)	
			#info = auth.get_account_info(user['idToken'])			
			#auth.send_email_verification(user['idToken'])
			#print(info)	
			user_information= {"username":username, "firstname":request.form["fname"],"lastname":request.form["lname"],"company":request.form["cname"],"industry":request.form["industry"],"contact":request.form["contact"],"url":request.form["url"],"emailverification":"pending","approval":"pending"} #removed role so that, signed up user does not have acccess to page
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
def forgotpassword:
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

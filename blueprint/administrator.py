from flask import Blueprint,redirect, url_for,render_template,send_from_directory, request,session,flash
import json
import requests
from blueprint.database import *

administrator = Blueprint('administrator', __name__, template_folder='templates')

@administrator.route("/administratoroverview")
def administratoroverview():
    if "user" in session and session["role"] == "administrator":
        all_active_accounts = get_all_store_owner_information_for_admin_overview()
        return render_template("landing_administrators.html",all_active_accounts=all_active_accounts,fullname=session["fullname"])
    return redirect("/pagenotfound")

@administrator.route("/managestoreowners")
def managestoreowners():
    if "user" in session and session["role"] == "administrator":
        all_owners = get_all_store_owner_information_for_manage_store_owner()
        return render_template("manage_store_owners_administrator.html",all_owners=all_owners,fullname=session["fullname"])
    elif "user" in session and session["role"] == "moderator":
        all_owners = get_all_store_owner_information_for_manage_store_owner()
        return render_template("manage_store_owners_moderator.html",all_owners=all_owners,fullname=session["fullname"])
    return redirect("/pagenotfound")

@administrator.route("/managemoderators")
def managemoderators():
    if "user" in session and session["role"] == "administrator":
        all_moderators = get_all_moderator_information_for_manage_moderator()
        return render_template("manage_moderators_administrator.html",all_moderators=all_moderators,fullname=session["fullname"])
    return redirect("/pagenotfound")

@administrator.route("/approverejectstoreowners")
def approverejectstoreowners():
    if "user" in session and session["role"] == "administrator":
        all_owners = get_all_store_owner_information_for_approve_reject()
        return render_template("approve_reject_store_owners_administrator.html",all_owners=all_owners,fullname=session["fullname"])
    elif "user" in session and session["role"] == "moderator":
        all_owners = get_all_store_owner_information_for_approve_reject()
        return render_template("approve_reject_store_owners_moderator.html",all_owners=all_owners,fullname=session["fullname"])
    return redirect("/pagenotfound")

@administrator.route("/createstoreowner", methods=["POST","GET"])
def createstoreowner():
    if request.method == "POST":
        username = request.form["username"].lower()
        password = request.form["password"]
        try:
            company = request.form["cname"]
            if check_if_company_name_unique(company):
                user_information= {"username":username,"deleteid":get_encrypted_id(password,username), "firstname":request.form["fname"],"lastname":request.form["lname"],"company":company,"industry":request.form["industry"],"contact":request.form["contact"],"url":request.form["url"],"status":True,"emailverification":True,"role":"store_owner"}
                register_user(username,password)
                create_store_owner(username,user_information)			
                flash("Store Owner Account Created Successfully!")
                return redirect("/managestoreowners")
            else:
                flash("Company Name already exists")
                return redirect("/managestoreowners")
        except requests.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            if error == "EMAIL_EXISTS":
                print("Email already exists")
                flash("Email already exists")			
            elif error == "TOO_MANY_ATTEMPTS_TRY_LATER":
                print("You have attempted too many times...")
                flash("You have attempted too many times...")
            return redirect("/managestoreowners")
    if "user" in session and session["role"] == "administrator" or session["role"] == "moderator":
        return redirect("/managestoreowners")
    return redirect("/pagenotfound")
    
@administrator.route("/deletestoreowner", methods=["POST","GET"])
def deletestoreowner():
    if request.method == "POST":
        delete_user_email = request.form["delete"]
        delete_store_owner(delete_user_email)			
        flash("Store Owner Account Deleted Successfully!")
        return redirect("/managestoreowners")
    if "user" in session and session["role"] == "administrator" or session["role"] == "moderator":
        return redirect("/managestoreowners")
    return redirect("/pagenotfound")

@administrator.route("/freezestoreowner", methods=["POST","GET"])
def freezestoreowner():
    if request.method == "POST":
        freeze_user_email = request.form["freeze"]
        freeze_unfreeze_store_owner(freeze_user_email)			
        flash("Store Owner Account has been status updated!")
        return redirect("/managestoreowners")
    if "user" in session and session["role"] == "administrator" or session["role"] == "moderator":
        return redirect("/managestoreowners")
    return redirect("/pagenotfound")

@administrator.route("/approvestoreowner", methods=["POST","GET"])
def approvestoreowner():
    if request.method == "POST":
        approve_user_email = request.form["approve"]
        approve_reject_user(approve_user_email,True)			
        flash("Store Owner Account has been approved!")
        return redirect("/managestoreowners")
    if "user" in session and session["role"] == "administrator" or session["role"] == "moderator":
        return redirect("/managestoreowners")
    return redirect("/pagenotfound")
    
@administrator.route("/rejectstoreowner", methods=["POST","GET"])
def rejectstoreowner():
    if request.method == "POST":
        reject_user_email = request.form["reject"]
        approve_reject_user(reject_user_email,False)			
        flash("Store Owner Account has been rejected!")
        return redirect("/managestoreowners")
    if "user" in session and session["role"] == "administrator" or session["role"] == "moderator":
        return redirect("/managestoreowners")
    return redirect("/pagenotfound")
 
@administrator.route("/createmoderator", methods=["POST","GET"])
def createmoderator():
    if request.method == "POST":
        username = request.form["username"].lower()
        password = request.form["password"]
        try:
            user_information= {"username":username,"deleteid":get_encrypted_id(password,username), "firstname":request.form["fname"],"lastname":request.form["lname"],"role":"moderator"}
            register_user(username,password)
            create_moderator(username,user_information)			
            flash("Moderator Account Created Successfully!")
            return redirect("/managemoderators")
        except requests.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            if error == "EMAIL_EXISTS":
                print("Email already exists")
                flash("Email already exists")			
            elif error == "TOO_MANY_ATTEMPTS_TRY_LATER":
                print("You have attempted too many times...")
                flash("You have attempted too many times...")
            return redirect("/managemoderators")
    if "user" in session and session["role"] == "administrator":
        return redirect("/managemoderators")
    return redirect("/pagenotfound")
    
@administrator.route("/deletemoderator", methods=["POST","GET"])
def deletemoderator():
    if request.method == "POST":
        delete_user_email = request.form["delete"]
        print(request.form)
        delete_moderator(delete_user_email)			
        flash("Moderator Account Deleted Successfully!")
        return redirect("/managemoderators")
    if "user" in session and session["role"] == "administrator":
        return redirect("/managemoderators")
    return redirect("/pagenotfound")
    

from flask import Blueprint,redirect, url_for,render_template,send_from_directory, request,session,flash
import json
import requests
from blueprint.database import *

problemReport = Blueprint('problemReport', __name__, template_folder='templates')

@problemReport.route("/problemreporting")
def problemreporting():
    if "role" in session and session["role"] == "store_owner":
        return render_template("problem_reporting.html",fullname=session["fullname"])
    elif "role" in session:
        return redirect("/")
    else:
        return redirect("/login") #if default user redirect to login first

@problemReport.route("/uploadissues", methods=["POST","GET"])
def uploadissues():
    if request.method=="POST":
        uploaded_files = request.files.getlist("file")
        description = request.form["problem"]
        check_file = True
        username = session["user"]
        for file in uploaded_files:
            if file.filename == "":
                continue
            if file.filename.split(".")[1] not in ["jpg","png","gif","jpeg"]:
                check_file = False    
        
        issue_information = {"id":retrieve_issue_id(username),"status":"Processing","description":description,"images":""}
        
        if check_file:
            upload_issue(username,uploaded_files,issue_information)
        else:
            flash("Unable to submit due to issues with uploaded images.")
            return redirect("/problemreporting")
            
        flash("Issue has been submitted for review.")
        return redirect("/problemreporting")
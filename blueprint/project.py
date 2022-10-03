from flask import Blueprint,redirect, url_for,render_template,send_from_directory, request,session,flash
import json
import requests
from blueprint.database import *

project = Blueprint('project', __name__, template_folder='templates')
@project.route("/createproject")
def createproject():
    project_name = request.form["pname"]
    category = request.form["category"]
    url = request.form["url"]
    username = session["username"]
    project_information = {retrieve_project_id(username) : {"pname":project_name,"category":category,"url":url}}
    try:
        set_project(username,project_information)
        #after setting project start to do crawl here
    except:
        print("failed to set project")

@project.route("/projectoverview")    
def projectoverview(): #need get rating and performance score oso
    if "role" in session and session["role"] == "store_owner":
        username = session["username"]
        store_owner_information = get_store_owner_information(username)
        all_projects = retreive_all_project(username)
        return render_template("landing_storeowners.html",store_owner_information=store_owner_information,all_projects=all_projects)
    elif "role" in session:
        return redirect("/")
    else:
        return redirect("/")

@project.route("/manageprojects")    
def manageprojects(): #need get rating and performance score oso
    if "role" in session and session["role"] == "store_owner":
        username = session["username"]
        project_lists = retreive_all_project(username)
        return render_template("manage_project.html",project_lists=project_lists)
    elif "role" in session:
        return redirect("/")
    else:
        return redirect("/")

@project.route("/deleteproject"):
def deleteproject():
    if "role" in session and session["role"] == "store_owner" and request.form["deleteProject"] != None:
        username = session["username"]
        deleteProjectID = request.form["deleteProject"] 
        delete_project_by_id(username,deleteProjectID)
        flash("Project Deleted...")
        return redirect("/manageprojects")
    elif "role" in session:
        return redirect("/")
    else:
        return redirect("/")
    
#@project.route() need a dynamic view detail pages that takes in username and project id
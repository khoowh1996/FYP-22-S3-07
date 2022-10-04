from flask import Blueprint,redirect, url_for,render_template,send_from_directory, request,session,flash
import json
import requests
from blueprint.database import *

project = Blueprint('project', __name__, template_folder='templates')

@project.route("/createproject", methods=["POST","GET"])
def createproject():
    if request.method == "POST":
        project_name = request.form["pname"]
        category = request.form["category"]
        url = request.form["url"]
        username = session["user"]
        project_information = {"id": retrieve_project_id(username),"pname":project_name,"category":category,"url":url}
        try:
            set_project(username,project_information)
            return redirect("/manageprojects")# might redirect to the created project or test item rating in future
            #after setting project start to do crawl here
        except:
            print("failed to set project")
    else:
        return render_template("create_project.html")

@project.route("/projectoverview")    
def projectoverview(): #need get rating and performance score oso
    if "role" in session and session["role"] == "store_owner":
        username = session["user"]
        store_owner_information = get_store_owner_information(username)
        all_projects = retrieve_all_project(username)
        return render_template("landing_storeowners.html",store_owner_information=store_owner_information,all_projects=all_projects)
    elif "role" in session:
        return redirect("/")
    else:
        return redirect("/")

@project.route("/manageprojects")    
def manageprojects(): #need get rating and performance score oso
    if "role" in session and session["role"] == "store_owner":
        username = session["user"]
        project_lists = retrieve_all_project(username)
        return render_template("manage_project.html",project_lists=project_lists)
    elif "role" in session:
        return redirect("/")
    else:
        return redirect("/")

@project.route("/deleteproject", methods=["POST","GET"])
def deleteproject():#need do a check if deleteprojectID does nto exist or project is empty
    if request.method == "POST":
        if "role" in session and session["role"] == "store_owner" and request.form["deleteProject"] != None:
            username = session["user"]
            deleteProjectID = request.form["deleteProject"] 
            delete_project_by_id(username,deleteProjectID)
            flash("Project Deleted...")
            return redirect("/manageprojects")
        elif "role" in session:
            return redirect("/")
        else:
            return redirect("/")
    else:
        return redirect("/")
    
#@project.route() need a dynamic view detail pages that takes in username and project id
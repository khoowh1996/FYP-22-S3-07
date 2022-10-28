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
        project_information = {"id": retrieve_project_id(username,session["role"]),"pname":project_name,"category":category,"url":url}
        try:
            set_project(username,project_information,session["role"])
            return redirect("/manageprojects")# might redirect to the created project or test item rating in future
            #after setting project start to do crawl here
        except:
            print("failed to set project")
    elif "role" in session and session["role"] == "store_owner" or session["role"] == "demo_user":
        return render_template("create_project.html",fullname=session["fullname"],role=session["role"] )
    elif "role" in session:
        return redirect("/")
    else:
        flash("Please login, before accessing to project dashboard")
        return redirect("/login") #if default user redirect to login first

@project.route("/projectoverview")    
def projectoverview(): #need get rating and performance score oso
    if "role" in session and session["role"] == "store_owner" or session["role"] == "demo_user":
        username = session["user"]
        store_owner_information = get_store_owner_information(username,session["role"])
        all_projects = retrieve_all_project(username,session["role"])
        all_issues = retrieve_all_user_issues(username,session["role"])
        return render_template("landing_storeowners.html",store_owner_information=store_owner_information,all_projects=all_projects,all_issues=all_issues)
    elif "role" in session and session["role"] == "sign_up_user":
        username = session["user"]
        store_owner_information = get_store_owner_information(username,session["role"])
        return render_template("landing_demousers.html",store_owner_information=store_owner_information,fullname=session["fullname"])
    elif "role" in session:
        return redirect("/")
    else:
        flash("Please login, before accessing to project dashboard")
        return redirect("/login") #if default user redirect to login first

@project.route("/manageprojects")    
def manageprojects(): #need get rating and performance score oso
    if "role" in session and session["role"] == "store_owner" or session["role"] == "demo_user":
        username = session["user"]
        project_lists = retrieve_all_project(username,session["role"])
        return render_template("manage_project.html",project_lists=project_lists,fullname=session["fullname"])
    elif "role" in session:
        return redirect("/") #if logged in non store owner user redirect to main page
    else:
        flash("Please login, before accessing to project dashboard")
        return redirect("/login") #if default user redirect to login first

@project.route("/deleteproject", methods=["POST","GET"])
def deleteproject():#need do a check if deleteprojectID does nto exist or project is empty
    if request.method == "POST":
        if request.form["deleteProject"] != None:
            username = session["user"]
            deleteProjectID = request.form["deleteProject"] 
            if get_project_by_id_exists(username,deleteProjectID,session["role"]): #check if the ProjectID exists,
                delete_project_by_id(username,deleteProjectID,session["role"])
                flash("Project Deleted...")
                return redirect("/manageprojects")
            else:
                flash("Project does not exist...")
                return redirect("/manageprojects")
    elif "role" in session and session["role"] == "store_owner" or session["role"] == "demo_user":
        return redirect("/manageprojects")
    elif "role" in session:
        return redirect("/") #if default user redirect to login first
    else:    
        flash("Please login, before any attempt for delete")
        return redirect("/") #user shouldnt be able to enter without the post.
    
@project.route("/project/<project_id>") #input username hash and project id to get the exact project details
def viewproject(project_id):
    if "role" in session and session["role"] == "store_owner" or session["role"] == "demo_user":
        username = session["user"]
        if get_project_by_id_exists(username,project_id,session["role"]): #to be redefined again database.py line 166
            project_information = get_project_by_id(username,project_id,session["role"])
            item_id = retrieve_item_id(username,project_id,session["role"])
            print(item_id)
            item_lists = retrieve_all_project_items(username,project_id,session["role"])
            return render_template("view_project.html",project_information=project_information,item_id=item_id,item_lists=item_lists,fullname=session["fullname"])
        return redirect("/manageprojects") #if store owner, but project not found redirect to manageprojects
    return redirect("/") #if not store owner redirect to homepage
    
@project.route("/project/<project_id>/item/<item_id>") #input username hash and project id to get the exact project details
def viewitem(project_id,item_id):
    if "role" in session and session["role"] == "store_owner" or session["role"] == "demo_user":
        username = session["user"]
        if get_project_by_id_exists(username,project_id,session["role"]): #to be redefined again database.py line 166
            project_information = get_project_by_id(username,project_id,session["role"])
            return render_template("test_item_rating.html",project_information=project_information,fullname=session["fullname"])
        return redirect("/project/"+project_id) #if store owner, but project not found redirect to manageprojects
    return redirect("/") #if not store owner redirect to homepage

@project.route("/createitem", methods=["POST","GET"])
def createitem():
    if request.method == "POST":
        item_name = request.form["name"]
        brand = request.form["brand"]
        price = request.form["price"]
        gender = request.form["gender"]
        age_group = request.form["agegroup"]
        project_id = request.form["project_id"]
        username = session["user"]
        print("project_id = " + project_id )
        item_id = retrieve_item_id(username,project_id,session["role"])
        item_information = {"id": item_id,"name":item_name,"brand":brand,"gender":gender,"price":price,"age_group":age_group}
        try:
            set_project_item(username,project_id,item_id,item_information,session["role"])
            return redirect("/project/"+project_id)
        except:
            print("failed to set item to project")
    elif "role" in session and session["role"] == "store_owner" or session["role"] == "demo_user":
        return redirect("/manageprojects")
    elif "role" in session:
        return redirect("/")
    else:
        flash("Please login, before accessing to project dashboard")
        return redirect("/login") #if default user redirect to login first
    
@project.route("/projectfaqs")
def projectfaq():
    if "role" in session and session["role"] == "store_owner" or session["role"] == "demo_user":
        faq_lists = get_faqs("store_owner")
        return render_template("store_owner_faqs.html",faq_lists=faq_lists,fullname=session["fullname"])
    else:
        flash("Please login before accessing project FAQS")
        return redirect("/login")
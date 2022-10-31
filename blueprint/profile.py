from flask import Blueprint,redirect, url_for,render_template,send_from_directory, request,session,flash
import json
import requests
from blueprint.database import *

profile = Blueprint('profile', __name__, template_folder='templates')

@profile.route("/userprofile")    
def userprofile(): #need get rating and performance score oso
    if "role" in session and (session["role"] == "store_owner" or session["role"] == "sign_up_user"):
        username = session["user"]
        store_owner_information = get_store_owner_information(username,session["role"])
        return render_template("view_profile.html",store_owner_information=store_owner_information)
    elif "role" in session:
        return redirect("/")
    else:
        flash("Please login, before accessing to project dashboard")
        return redirect("/login") #if default user redirect to login first

@profile.route("/updateprofile", methods=["POST","GET"])
def updateprofile():
    if request.method == "POST":
        username = session["user"]        
        user_information= {"firstname":request.form["fname"],"lastname":request.form["lname"],"company":request.form["cname"],"industry":request.form["industry"],"contact":request.form["contact"],"url":request.form["url"]}
        update_user_information(username,user_information,session["role"])
        flash("Profile Updated Successfully!")#need to add to view profile flash message
        return redirect("/userprofile")        
    elif "role" in session and (session["role"] == "store_owner" or session["role"] == "sign_up_user"):
        return redirect("/userprofile")
    elif "role" in session:
        return redirect("/userprofile") #if default user redirect to login first
    else:    
        flash("Please login, before any attempt for update")
        return redirect("/") #user shouldnt be able to enter without the post.
        
@profile.route("/managesubscription")    
def managesubscription(): #need get rating and performance score oso
    if "role" in session and session["role"] == "store_owner":
        username = session["user"]
        return render_template("manage_subscription.html",subscription_information=get_owner_subscription_information(username),fullname=session["fullname"])
    elif "role" in session and session["role"] == "sign_up_user":
        return redirect("/subscription")
    elif "role" in session:
        return redirect("/") #if logged in non store owner user redirect to main page
    else:
        flash("Please login, before accessing to project dashboard")
        return redirect("/login") #if default user redirect to login first
        
@profile.route("/autorenew",methods=["POST","GET"])
def autorenew():
    if request.method == "POST":       
        username = session["user"]
        if request.form["renew"] == "false": #using string cause not sure how to take actual boolean
            print("set auto renew to false")
            update_auto_renew_subscription(username,False)
        elif request.form["renew"] == "true": #using string cause not sure how to take actual boolean
            print("set auto renew to true")
            update_auto_renew_subscription(username,True)
        flash("Auto Renew Subscription has been updated.")
        return redirect("/managesubscription")
    return redirect("/managesubscription")
    
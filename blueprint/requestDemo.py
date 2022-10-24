from flask import Blueprint,redirect, url_for,render_template,send_from_directory, request,session,flash
import json
import requests
from blueprint.database import *

requestDemo = Blueprint('requestDemo', __name__, template_folder='templates')
@requestDemo.route("/demo", methods=["POST","GET"])
def request_demo():
    if request.method == "POST":
        username = request.form["email"]
        if demo_user_exist(username):
            print("user is already in demo")
            flash("Email already exists, you already registered for demo!")      
            return redirect("/demo")
        else:
            demo_username,demo_password = createDemoAccount()
            user_information= {"role":"demo_user","email":username,"phonenumber":request.form["phone_number"], "firstname":request.form["fname"],"lastname":request.form["lname"],"country":request.form["country"],"url":request.form["url"],"comment":request.form["comment"],"requesteddate":date.today().strftime("%d/%m/%Y"),"demo_username":demo_username,"demo_password":demo_password, }
            set_demo_user(username,user_information)
            return redirect("/mail?user="+username)     
    return render_template("request_demo.html")

@requestDemo.route("/faq")
def faq():
    faq_lists = get_faqs("default_user")
    return render_template("faq.html",faq_lists=faq_lists)

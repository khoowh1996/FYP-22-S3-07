from flask import Blueprint,redirect, url_for,render_template,send_from_directory, request,session,flash
import json
import requests
from blueprint.database import *

subscriptionPlan = Blueprint('subscriptionPlan', __name__, template_folder='templates')
@subscriptionPlan.route("/subscription")
def subscription(): 
    monthly_pricing = get_pricing("monthly")
    yearly_pricing = get_pricing("yearly")
    try:
        role = session["role"]
    except:
        role = ""
    return render_template("subscription_plan.html",monthly_pricing=monthly_pricing,role=role,yearly_pricing=yearly_pricing)

@subscriptionPlan.route("/payment")
def payment():
    if "user" not in session:
        flash("Please login before payment.")
        return redirect("/login")
    if request.args.get("subscribe") != None:    
        subscription_type = request.args.get("subscribe")
        print("is not empty")
        session["subscription_type"] = subscription_type
    
    if "user" in session and session["role"] == "store_owner" and "subscription_type" in session:
        if check_user_subscription(session["user"],session["subscription_type"],session["role"]): #if False it means different plan
            return render_template("payment.html",role=session["role"],subscription_type=session["subscription_type"])
        else:
            flash("You are currently subscribed to the same plan as you had chosen.")
            session.pop("subscription_type",None)
            return redirect("/subscription")
    elif "user" in session and session["role"] == "store_owner" and "subscription_type" not in session:
        flash("Please choose a subscription plan first")
        return redirect(url_for("subscriptionPlan.subscription"))
        
    if "user" in session and session["role"] == "sign_up_user" and "subscription_type" in session:
        if check_user_subscription(session["user"],session["subscription_type"],session["role"]): #if False it means different plan
            return render_template("payment.html",role=session["role"],subscription_type=session["subscription_type"])
        else:
            flash("You are currently subscribed to the same plan as you had chosen.")
            session.pop("subscription_type",None)
            return redirect("/subscription")
    elif "user" in session and session["role"] == "sign_up_user" and "subscription_type" not in session:
        flash("Please choose a subscription plan first")
        return redirect(url_for("subscriptionPlan.subscription"))

    flash("Please login before payment.")
    session["url"] = "/payment"
    return redirect("/login")
    
    
@subscriptionPlan.route("/paymentFinalized",methods=["POST","GET"])
def payment_finalized():
    if "user" in session and "subscription_type" in session and "role" in session:
        session.pop("subscription_type",None)
        username = session["user"]
        print(request.form["pay"])
        set_subscription(username,request.form["pay"],session["role"])
        flash("Payment success, Subscription has started. Email will be send to you for notification")    
        #return redirect("/")
        return redirect("/mail?user="+username+"&name="+session["fullname"]+"&EmailTemplate=payment_success") 
    elif "user" in session and "subscription_type" not in session:
        flash("Please choose a subscription plan first")
        return redirect(url_for("subscriptionPlan.subscription"))
    else:
        flash("Please login before payment.")
        return redirect(url_for("authentication.login"))
        
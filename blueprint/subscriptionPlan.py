from flask import Blueprint,redirect, url_for,render_template,send_from_directory, request,session,flash
import json
import requests
from blueprint.database import *

subscriptionPlan = Blueprint('subscriptionPlan', __name__, template_folder='templates')
@subscriptionPlan.route("/subscription")
def subscription(): 
    monthly_pricing = get_monthly_pricing()
    yearly_pricing = get_yearly_pricing()
    return render_template("subscription_plan.html",monthly_pricing=monthly_pricing,yearly_pricing=yearly_pricing)

@subscriptionPlan.route("/payment")
def payment():
    if "role" not in session:
        flash("login before choosing!")
        return redirect("/login")
    if request.args.get("subscribe") != None:    
        subscription_type = request.args.get("subscribe")
        print("is not empty")
        session["subscription_type"] = subscription_type
    
    if "user" in session and "subscription_type" in session:
        return render_template("payment.html",subscription_type=session["subscription_type"])
    elif "user" in session and "subscription_type" not in session:
        flash("Please choose a subscription plan first")
        return redirect(url_for("subscriptionPlan.subscription"))
    flash("Please login for payment.")
    session["url"] = url_for("payment")
    return redirect("/login")
    
    
@subscriptionPlan.route("/paymentFinalized",methods=["POST","GET"])
def payment_finalized():
    if "user" in session and "subscription_type" in session:
        session.pop("subscription_type",None)
        username = session["user"]
        print(request.form["pay"])
        update_payment(username,request.form["pay"])
        flash("Payment success, Subscription has started. Email will be send to you for notification")    
        return redirect("/")
    elif "user" in session and "subscription_type" not in session:
        flash("Please choose a subscription plan first")
        return redirect(url_for("subscriptionPlan.subscription"))
    else:
        return redirect(url_for("authentication.login"))
        
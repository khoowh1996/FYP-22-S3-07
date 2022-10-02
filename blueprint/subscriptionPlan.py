from flask import Blueprint,redirect, url_for,render_template,send_from_directory, request,session,flash
import json
import requests
from blueprint.database import *

subscriptionPlan = Blueprint('subscriptionPlan', __name__, template_folder='templates')
@subscriptionPlan.route("/subscription")
def subscription(): 
    return render_template("subscription_plan.html")

@subscriptionPlan.route("/payment")
def payment():    
    if "user" in session:
        render_template("payment.html")
    redirect(url_for("authentication.login"))
    
@subscriptionPlan.route("/paymentFinalized")
def payment_finalized():
    flash("Payment success, Subscription has started. Email will be send to you for notification")    
    redirect("/")
    
from flask import Blueprint,redirect, url_for,render_template,send_from_directory, request,session,flash
import json
import requests
from blueprint.database import *

subscriptionPlan = Blueprint('subscriptionPlan', __name__, template_folder='templates')
@subscriptionPlan.route("/subscription")
def subscription(): 
    return render_template("subscription_plan.html")


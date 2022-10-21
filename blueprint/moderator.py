from flask import Blueprint,redirect, url_for,render_template,send_from_directory, request,session,flash
import json
import requests
from blueprint.database import *

moderator = Blueprint('moderator', __name__, template_folder='templates')

@moderator.route("/moderatoroverview")
def moderatoroverview():
    if "user" in session and session["role"] == "moderator":
        all_active_accounts = get_all_store_owner_information_for_admin_overview()
        return render_template("landing_moderators.html",all_active_accounts=all_active_accounts,fullname=session["fullname"])
    return redirect("/pagenotfound")

#@moderator.route("/problemsreported")
#def moderatoroverview():
#   if "user" in session and session["role"] == "moderator":
#        all_active_accounts = get_all_store_owner_information_for_admin_overview()
#        return render_template("landing_moderators.html",all_active_accounts=all_active_accounts,fullname=session["fullname"])
#    return redirect("/pagenotfound")

    

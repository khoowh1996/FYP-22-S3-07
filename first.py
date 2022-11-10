from flask import Flask,redirect, url_for,render_template,send_from_directory, request, session,flash
from flask_mail import Mail, Message
from blueprint.authentication import authentication
#from blueprint.upload import upload
from blueprint.requestDemo import requestDemo
from blueprint.subscriptionPlan import subscriptionPlan
from blueprint.project import project
from blueprint.profile import profile
from blueprint.problemReport import problemReport
from blueprint.administrator import administrator
from blueprint.moderator import moderator
from datetime import timedelta
import os
import secrets
import string
from blueprint.database import *

app = Flask(__name__, static_folder="static")
key = "qwertyuiopasdfghjklzxcvbnm!2"#''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(32))
app.secret_key = key
app.config["SESSION_COOKIE_PATH"] = "/"
app.config["SESSION_COOKIE_SAMESITE"] = None
app.config["SESSION_COOKIE_SECURE"] = True
app.permanent_session_lifetime = timedelta(hours=1)
app.register_blueprint(authentication)
#app.register_blueprint(upload)
app.register_blueprint(requestDemo)
app.register_blueprint(subscriptionPlan)
app.register_blueprint(project)
app.register_blueprint(profile)
app.register_blueprint(problemReport)
app.register_blueprint(administrator)
app.register_blueprint(moderator)
@app.route("/")
def home():
    #return "<h1>Hello</h1>"
    #login_as_store_owner_now()
    try:
        role = session["role"] 
    except:
        role = ""
    return render_template("index.html",role=role)

def login_as_store_owner_now():
    session["user"] = "khoowh1996@gmail.com"
    session["password"] = "qwertyuiop!2"
    user = session["user"]
    password = session["password"]
    user_information = get_general_user_information(user)
    session["role"] = user_information["role"] 
    session["fullname"] = user_information["fullname"] 
    
@app.route('/<path:path>')
def static_file(path):
    return send_from_directory(app.static_folder, path)

@app.route('/project/<path:path>')
def static_file_for_project(path):
    return send_from_directory(app.static_folder, path) 

#@app.route("/<name>")
#def browse(name):
#    list_of_files = os.listdir('./templates/')
#    list_of_html_files = []
#    for files in list_of_files:
#        if files.endswith('.html') and (name+".html" == files or name == files):
#            return render_template(files)
#   return redirect(url_for("pagenotfound"))

@app.route("/pagenotfound")
def pagenotfound():
    return f"404 Error! Page Not Found"

@app.route("/admin")
def admin():
    return redirect(url_for("pagenotfound"))


mail = Mail(app) # instantiate the mail class

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'myrecommendservices@gmail.com'
app.config['MAIL_PASSWORD'] = 'lltmhynhbspezyqu'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['TESTING'] = False
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['DEBUG'] = False
mail = Mail(app)

@app.route("/mail")
def sendmail():
    email_template = request.args.get("EmailTemplate")
    if email_template == "demo":
        username = request.args.get("user")
        demo_user = request.args.get("demo_user")
        
        name,demo_username,demo_password = get_demo_information(demo_user)
        with mail.connect() as conn:
            msg = Message(
                            'Hello This is MyRecommend Notification for Demo',
                            sender ='myrecommendservices@gmail.com',
                            recipients = [username]
                        )
            msg.body = 'Hello {},\n\nThe following is the demo account information to login to our Demo Dashboard.\nDemo Username : {} \nDemo Password : {} \n\nFor any more information, do contact our customer services at myrecommendservices@gmail.com'.format(name,demo_username,demo_password)
            conn.send(msg)
        flash("Request Demo Email Sent... Please login with your demo account")
        return redirect(url_for("authentication.login"))
    elif email_template == "approved":        
        username = request.args.get("user")
        name = request.args.get("name")
        with mail.connect() as conn:
            msg = Message(
                            'MyRecommend Notification on Account approval',
                            sender ='myrecommendservices@gmail.com',
                            recipients = [username]
                        )
            msg.body = 'Hello {},\n\nYour account has been approved by our moderators.\nPlease kindly login to our system to start using our features.\nIf you have not subscribed, do kindly navigate to https://www.myrecommend.herokuapp.com/subscriptionPlan to select plan.\n\nFor any more information, do contact our customer services at myrecommendservices@gmail.com'.format(name)
            conn.send(msg)
        flash("Notification Email has been Sent to store owner...")
        return redirect("/managestoreowners")
    elif email_template == "rejected":    
        username = request.args.get("user")
        name = request.args.get("name")        
        with mail.connect() as conn:
            msg = Message(
                            'MyRecommend Notification on Account approval',
                            sender ='myrecommendservices@gmail.com',
                            recipients = [username]
                        )
            msg.body = 'Hello {},\n\nYour account has been rejected by our moderators.\nFor any more details information, do contact our customer services at myrecommendservices@gmail.com'.format(name)
            conn.send(msg)
        flash("Notification Email has been Sent to store owner...")
        return redirect("/managestoreowners")
    elif email_template == "payment_success":
        username = request.args.get("user")
        name = request.args.get("name")
        with mail.connect() as conn:
            msg = Message(
                            'MyRecommend Notification on Account subscription status',
                            sender ='myrecommendservices@gmail.com',
                            recipients = [username]
                        )
            msg.body = 'Hello {},\n\nYou have started your subscription!\nPlease login to our website at https://myrecommend.herokuapp.com/login.\nIf your account has not been approved, Please allow up to 3 business days for your account to be approved. The account expiry will start after account has been approved.\n\nDo contact our customer services at myrecommendservices@gmail.com, for any issues encountered or information.\n'.format(name)
            conn.send(msg)
        flash("Subscription Email has been Sent...")
        return redirect("/login")
    elif email_template == "freezed":    
        username = request.args.get("user")
        name = request.args.get("name")
        with mail.connect() as conn:
            msg = Message(
                            'MyRecommend Notification on Account status',
                            sender ='myrecommendservices@gmail.com',
                            recipients = [username]
                        )
            msg.body = 'Hello {},\n\nYour account has been freezed, Due to a violation of our Usage Policy.\nDo reply or contact our customer services at myrecommendservices@gmail.com, for more information.\n'.format(name)
            conn.send(msg)
        flash("Subscription Email has been Sent...")
        return redirect("/managestoreowners")
        
    elif email_template == "unfreezed":
        username = request.args.get("user")
        name = request.args.get("name")
        with mail.connect() as conn:
            msg = Message(
                            'MyRecommend Notification on Account status',
                            sender ='myrecommendservices@gmail.com',
                            recipients = [username]
                        )
            msg.body = 'Hello {},\n\nYour account has been unfreezed!\nOur moderators has reviewed your case and has rescind status.\nPlease login to our website at https://myrecommend.herokuapp.com/login.\n\nDo reply or contact our customer services at myrecommendservices@gmail.com, for more information.\n'.format(name)
            conn.send(msg)
        flash("Subscription Email has been Sent...")
        return redirect("/managestoreowners")
        
@app.route("/contactus",methods=["POST","GET"])
def contactus():
    if request.method == "POST":
        fullname = request.form["fname"] + " " + request.form["lname"]
        email = request.form["email"]
        email_subject = request.form["subject"]
        email_body = request.form["body"]
        with mail.connect() as conn:
            msg = Message(
                            email_subject + " to " + email,
                            sender ='myrecommendservices@gmail.com',
                            recipients = ['myrecommendservices@gmail.com','khoowh1996@gmail.com']
                        )
            msg.body = 'Hello {},\n\nWe have recieve the email for the following\n{}\n\ndo contact our customer services at myrecommendservices@gmail.com'.format(fullname,email_body)
            conn.send(msg)
        flash("Email has been sent to our representative.")
        return redirect("/")
    try:
        role = session["role"]
    except:
        role = ""
    return render_template("contactus.html",role=role)
    
@app.route("/about")
def about():
    try:
        role = session["role"]
    except:
        role = ""
    return render_template("about.html",role=role)

if __name__ == "__main__":
    app.run()
    
    

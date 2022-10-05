from flask import Flask,redirect, url_for,render_template,send_from_directory, request, session,flash
from flask_mail import Mail, Message
from blueprint.authentication import authentication
from blueprint.upload import upload
from blueprint.requestDemo import requestDemo
from blueprint.subscriptionPlan import subscriptionPlan
from blueprint.project import project
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
app.register_blueprint(upload)
app.register_blueprint(requestDemo)
app.register_blueprint(subscriptionPlan)
app.register_blueprint(project)
@app.route("/")
def home():
    #return "<h1>Hello</h1>"
    #login_as_store_owner_now()
    return render_template("index.html")

def login_as_store_owner_now():
    session["user"] = "khoowh1996@gmail.com"
    session["password"] = "qwertyuiop!2"
    user = session["user"]
    password = session["password"]
    user,user_information = login_user(user,password)
    session["role"] = user_information["role"] 
    session["fullname"] = user_information["fullname"] 
    
@app.route('/<path:path>')
def static_file(path):
    return send_from_directory(app.static_folder, path)

@app.route('/project/<path:path>')
def static_file_for_project(path):
    return send_from_directory(app.static_folder, path) 
  
@app.route("/<name>")
def browse(name):
    list_of_files = os.listdir('./templates/')
    list_of_html_files = []
    for files in list_of_files:
        if files.endswith('.html') and (name+".html" == files or name == files):
            return render_template(files)
    return redirect(url_for("pagenotfound"))

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
    username = request.args.get("user")
    name,demo_username,demo_password = get_demo_information(username)
    with mail.connect() as conn:
        msg = Message(
                        'Hello This is MyRecommend Notification for Demo',
                        sender ='myrecommendservices@gmail.com',
                        recipients = ['khoowh1996@gmail.com']
                    )
        msg.body = 'Hello {},\n\nThe following is the demo account information to login to our Demo Dashboard.\nDemo Username : {} \nDemo Password : {} \n\nFor any more information, do contact our customer services at myrecommendservices@gmail.com'.format(name,demo_username,demo_password)
        conn.send(msg)
    flash("Request Demo Email Sent... Please login with your demo account")
    return redirect(url_for("authentication.login"))

if __name__ == "__main__":
    app.run()
    
    

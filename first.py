from flask import Flask,redirect, url_for,render_template,send_from_directory, request, session
from blueprint.authentication import authentication
from datetime import timedelta
import os
import secrets
import string

app = Flask(__name__)
key = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(32))
app.secret_key = key
app.permanent_session_lifetime = timedelta(hours=1)
app.register_blueprint(authentication)
@app.route("/")
def home():
    #return "<h1>Hello</h1>"
    return render_template("index.html")

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)
    
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

#@app.route("/login", methods=["POST","GET"])
#def login():
#    if request.method == "POST":
#        session.permanent = True
#        user = request.form["username"]
#        password = request.form["password"]
#        session["user"] = user
#        session["password"] = password
#        return redirect(url_for("user"))
#    if "user" in session:
#        return redirect(url_for("user"))
#    return render_template("login.html")
#
#@app.route("/logout")
#def logout():
#    session.pop("user",None)
#    session.pop("password",None)
#    return redirect(url_for("login"))
#
#@app.route("/user")
#def user():
#    if "user" in session:
#        user = session["user"]
#        password = session["password"]
#        return f"<h1>{user}</h1><h1>{password}</h1></n> <h1>{key}</h1>"
#    return redirect(url_for("login"))

@app.route("/admin")
def admin():
    return redirect(url_for("pagenotfound"))

if __name__ == "__main__":
    app.run()
    
    
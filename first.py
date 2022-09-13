from flask import Flask,redirect, url_for,render_template,send_from_directory, request, session
from blueprint.authentication import authentication
#from blueprint.upload import upload
from datetime import timedelta
import os
import secrets
import string

app = Flask(__name__)
key = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(32))
app.secret_key = key
app.permanent_session_lifetime = timedelta(hours=1)
app.register_blueprint(authentication)
app.register_blueprint(upload)
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

@app.route("/admin")
def admin():
    return redirect(url_for("pagenotfound"))

if __name__ == "__main__":
    app.run()
    
    

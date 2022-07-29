from flask import Flask,redirect, url_for,render_template,send_from_directory
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello</h1>"

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)
    
@app.route("/<name>")
def user(name):
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
    
    
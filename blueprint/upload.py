from flask import Blueprint,redirect, url_for,render_template,send_from_directory, request,session
import pyrebase

config = {
"apiKey": "AIzaSyB3EuVdoM4dHQCUwEYScbvbnxiXGXObdnc",
"authDomain": "fyp-22-s3-07.firebaseapp.com",
"databaseURL": "https://fyp-22-s3-07-default-rtdb.asia-southeast1.firebasedatabase.app",
"projectId": "fyp-22-s3-07",
"storageBucket": "fyp-22-s3-07.appspot.com",
"serviceAccount": "blueprint\serviceAccountKey.json"
}

firebase_storage = pyrebase.initialize_app(config)
storage = firebase_storage.storage()

upload = Blueprint("upload", __name__, template_folder="templates")
@upload.route("/upload")
def uploadFile():  
    return render_template("file_upload_form.html")  

@upload.route("/success", methods=["POST"])  
def success():  
    if request.method == "POST":  
        f = request.files['file']
        storage.child(f.filename).put(f)
        return render_template("success.html", name = f.filename)  


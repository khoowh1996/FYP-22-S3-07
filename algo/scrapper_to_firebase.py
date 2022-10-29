#-------------------------------------------------------------------------------
# Imports
import pyrebase
import urllib

#-------------------------------------------------------------------------------
# Variables & Setup



config = {
"apiKey": "AIzaSyB3EuVdoM4dHQCUwEYScbvbnxiXGXObdnc",
"authDomain": "fyp-22-s3-07.firebaseapp.com",
"databaseURL": "https://fyp-22-s3-07-default-rtdb.asia-southeast1.firebasedatabase.app",
"projectId": "fyp-22-s3-07",
"storageBucket": "fyp-22-s3-07.appspot.com",
"serviceAccount": "serviceAccountKey.json"
}

firebase_storage = pyrebase.initialize_app(config)
storage = firebase_storage.storage()

#url = storage.child("test.csv").get_url(None)  # getting the url from storage
#print(url)  # printing the url
#text_file = urllib.request.urlopen(url).read()  # reading the csv file
#print(text_file)
def upload(filename,file):
    storage.child(filename).put(file)
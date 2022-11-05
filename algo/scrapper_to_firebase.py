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

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
database = firebase.database()
#url = storage.child("test.csv").get_url(None)  # getting the url from storage
#print(url)  # printing the url
#text_file = urllib.request.urlopen(url).read()  # reading the csv file
#print(text_file)
def upload(filename,file):
    storage.child(filename).put(file)

def download_csv():
    txt_url = storage.child("main_dataset.csv").get_url(None)
    webpage = urllib.request.urlopen(txt_url)

    with open("main_dataset.csv", mode='w') as f:
        for line in webpage:            
            f.write(line.decode('utf-8').rstrip()+"\n")
            
def stream_handler(message):
    #print(message["event"]) # put
    #print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    #print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
    #for item,val in message["data"].items():
    #    print(val["url"]+","+val["crawler"])
    try:
        with open('crawl_lists.txt','a') as f:
            for item,val in message["data"].items():
                f.write(val["url"]+","+val["crawler"]+"\n")
                database.child("crawl_lists").child(item).remove()
    except AttributeError as e:
        print("no crawl list to crawl.")
    
def start_stream():
    my_stream = database.child("crawl_lists").stream(stream_handler)
    my_stream.close()
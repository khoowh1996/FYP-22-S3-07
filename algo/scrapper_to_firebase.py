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
"serviceAccount": {
                  "type": "service_account",
                  "project_id": "fyp-22-s3-07",
                  "private_key_id": "d393898bb68249d748c99bc5709a0e6951506191",
                  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCXrd+4CMUmsOx4\nuVXaFt27wOrt8eh50lixHCHtzYqTc/ETf/1B65YirNIfIoxOKdQ3yPb0XEtZtdD1\nitBDOAubfOUUJSHAcZ0aC6kSMVidMy7/QH781nJmkDf4TTi/0iRJfoXew8PE8XLt\nGSQ+azyTcHT4Tm5aKVwKwk6zrK2ygobrK1umNzmq/p7nse/d1MDNppCY+QDGlU0m\nVKyGh2PXHicXxTe1tovtlEmHwP7cpNzSfvKHxxcdvwuN6Rq1wYDWW4bxA8y/5j6D\nM83kB1TQXsDQp2kZoxW9o4OucF4uolCJjkpCDU7jrCTuie2L1nqf/pNlCq2j7GY3\nR+MjmoFLAgMBAAECggEAJ36CILDD6PmrcRnNBW7ryG4InfFdt46yQleRbBKXcSKA\n1LOAVbBKlPfL9Ihx4Q5aMDZXOzRm+FJzuOOuq7oFp7RjD5ZFjg7nObdsjAymRrRj\nmdoI1rvd6N/HexNcYfINOcfEgscVjAvUgXEI82nHyZpAEsGVUUuwqCqFBJrDVZXp\ndGhmhfea5xGtmwjL9pbR1IG/oIwhZUKuELhY44aCSvFhiUF+H315jFP6T3QFsx4d\n+cAhgJPdr2gnKHLlx8OTk3Ok4WOFAoxJiB3X/AzrXlfpZIZ8D+MEoyDZKleEdbw/\nef5Rgr1elfySIKHUHW4iyyBYC3OFTnWFN+GxwJedxQKBgQDKfJauwfOqHH4fmIkh\nZUmiRwdsAxImfrJFp+KvzIcHhBlk0EKIKaCbnyNv/A46LRVnvS4TgR74lAI0HdVi\nZw8qbf4c41ppel28jdbpwkSYnmARz8YvZSBXmG7o9ieYp9vhrXIjlwGhYTvorBoU\n2ogCXvTKy5JyQsUG/4UP4pjaTQKBgQC/w9x7pl8i32vG7NS0tPHBiBsMk/wzg4aY\n/7fN8AKCNlrXE9Is1fvOB68XMnJuKu5pF1rExuxQYqFP5OGK6q5bX3U9ZGd4juzz\nowbajBh60CQG/ZTKFdtb0CrbMfgvMEdNwSWphXmjCGkblv7sZMsFCwG9cO77sHED\nfXnoDL3l9wKBgDiRh/M4oh8jKKUhEyZuSpz4ZP1q+jYg7SMCnRTp+ctCv2lnuT6b\nCpCPa/IMI9li4PkDZAz05Lcjel4e+48rJZR/+B8P8SFIm0ljAuh5anqMvGAdgMua\n3+c44btZkYRXWNl6gEmrFTyFkpwVAJBU4OxwpMjHCJm9R5gF6KGgd319AoGAZx4C\nLLd9BvqPMQvfIUD/kysGKJBXGLhMI2+2vdWm87AYzvjIlvWGDvcQzu+Amv8Y7ofx\ndkjlgCBZT+Xq5lFl6pp9J8Ma5LgucKCkqdaVv0y3Ys7vOG/iYg+hS/cl1vImFYic\nIPk2PFXkd0KN2D4m8ZJGoEDfMZZiXxcU+5QGdWcCgYAC53fSACqsWBt2bvZatrCn\ncsgmb8qEREOx5NtilXN3pKdyshMU3J+UEfpNWYuz+yvuUhbWFXW4Z9ZXhvbGJbRd\nuZiV0NMnGIpoYvpTnkRPfWYqKSrzvhrPj8m+L+T4QDL0WiyGG00yoR+2ij4PjWex\ndTJ6pmFVoI/Lt+i7ZXOgSg==\n-----END PRIVATE KEY-----\n",
                  "client_email": "admin-369@fyp-22-s3-07.iam.gserviceaccount.com",
                  "client_id": "113990616481744999778",
                  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                  "token_uri": "https://oauth2.googleapis.com/token",
                  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/admin-369%40fyp-22-s3-07.iam.gserviceaccount.com"
                }

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

    with open("main_dataset.csv", mode='w', encoding='utf-8') as f:
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
                f.write(val["url"]+","+val["crawler"]+","+val["projectcsv"]+"\n")
                database.child("crawl_lists").child(item).remove()
    except AttributeError as e:
        print("no crawl list to crawl.")
    
def start_stream():
    my_stream = database.child("crawl_lists").stream(stream_handler)
    my_stream.close()
import pandas as pd
from math import sqrt
import csv
from collections import defaultdict
import pyrebase
import urllib
import io

# Config to read file from firebase storage
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

url = storage.child("Demo.csv").get_url(None)  # getting the url from storage
webpage = urllib.request.urlopen(url)

# Read the CSV file
#reader = csv.DictReader(open(r'C:\Users\khoow\OneDrive\Desktop\flask\web1\algo\Demo.csv'))
reader = csv.DictReader(io.TextIOWrapper(webpage)) #read from the url
dataset = defaultdict(dict)

# Put it in a dictionary
for i in reader:
    dataset[i['product_name'].strip()][i['user name'].strip()] = i['rating'].strip()

# If you want to see it in clearer view
#dataFrame = pd.DataFrame(dataset)
#dataFrame.fillna('No Ratings', inplace = True)
#print(dataFrame)

# To see the whole dictionary of the data from CSV
print(dataset)

# Get unique set of items bought
def uniqueItems():
    uniqueItemList = []
    for p in dataset.keys():
        for i in dataset[p]:
            uniqueItemList.append(i)
    s = set(uniqueItemList)
    uniqueItemList = list(s)
    return uniqueItemList

# To see what items are bought
#print(uniqueItems())

# To get the ratings of each item
'''
for i in dataset.values():
    for j in i.values():
        print (j)
'''
# To get all values of 1 person
#for i in dataset.values():
    #print (i)


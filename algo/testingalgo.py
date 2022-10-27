from operator import index, indexOf
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

#firebase_storage = pyrebase.initialize_app(config)
#storage = firebase_storage.storage()

#url = storage.child("Demo.csv").get_url(None)  # getting the url from storage
#webpage = urllib.request.urlopen(url)

# Read the CSV file
reader = csv.DictReader(open(r'C:\Users\lyhe1\Documents\GitHub\FYP-22-S3-07\algo\Demo.csv'))
#reader = csv.DictReader(io.TextIOWrapper(webpage)) #read from the url
dataset = defaultdict(dict)

# Put it in a dictionary
for i in reader:
    dataset[i['user name'].strip()][i['product_category'].strip()] = i['rating'].strip()

ownerinput1 = 'highheels'
ownerinput2 = 'sneakers'

# If you want to see it in clearer view
#dataFrame = pd.DataFrame(dataset)
#dataFrame.fillna('No Ratings', inplace = True)
#print(dataFrame)

# To see the whole dictionary of the data from CSV
#print(dataset)

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
#for i in dataset.values():
#    for j in i.values():
#        print (j)

# To get every person in dictionary
#for i in dataset:
#    print (i)

# To get all ratings of each person
#for i in dataset.values():
#    print (i)

listOfValues = []
#print(dataset['Marina'][ownerinput2])
def getAvgRating(dataset):
    for i in dataset.values():
        if ownerinput2 in i.keys():
            if ownerinput1 in i.keys():
                listOfValues.append(int(i[ownerinput1]))
    if sum(listOfValues) == 0 or len(listOfValues) == 0:
        print('No one has bought', ownerinput1,'among people who has bought',ownerinput2)
    else:
        avg = sum(listOfValues) / len(listOfValues)
        print('The average rating of', ownerinput1,'among people who has bought', ownerinput2 , 'is', avg)

getAvgRating(dataset)
from operator import index, indexOf
from queue import Empty
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
    dataset[i['user name'].strip()][i['product_category'].replace(' ','')] = i['rating'].replace(' ','')

ownerinput1 = 'highheels'
ownerinput2 = ''

# If you want to see it in clearer view
#dataFrame = pd.DataFrame(dataset)
#dataFrame.fillna('No Ratings', inplace = True)
#print(dataFrame)

# To see the whole dictionary of the data from CSV
#print(dataset)

# Get unique set of items bought
def uniqueCategories():
    uniqueCategoriesList = []
    for p in dataset.keys():
        for i in dataset[p]:
            uniqueCategoriesList.append(i)
    s = set(uniqueCategoriesList)
    uniqueCategoriesList = list(s)
    return uniqueCategoriesList

#print(dataset['Marina'][ownerinput2])
def compareWithOne(dataset, input1, input2):
    listOfValues = []
    for i in dataset.values():
        # Find who has bought both items that is stated in the arguments
        if input2 in i.keys():
            if input1 in i.keys():
                # Get their values and put all into the list
                listOfValues.append(float(i[input1]))
    # To handle the exception of division by 0
    if len(listOfValues) == 0:
        print('No one has bought', input1,'among people who has bought',input2)
    else:
        avg = sum(listOfValues) / len(listOfValues)
        if avg <= 2.5:
            print('This category of items,', input1, 'will not do well among people who has bought', input2, 'as the average rating is', avg)
        elif avg < 4.0:
            print('This category of items,', input1, 'will be average among people who has bought', input2, 'as the average rating is', avg)
        elif 4.0 <= avg:
            print('This category of items,', input1, 'will do very well among people who has bought', input2, 'as the average rating is', avg)
    listOfValues.clear()

def compareWithAllItems():
    itemList = uniqueCategories()
    # Remove the item that the owner wants rating of
    for i in itemList:
        if i == ownerinput1:
            itemList.remove(i)
    # Now compare it to all other items
    for item in itemList:
        compareWithOne(dataset, ownerinput1, item)

if ownerinput2 == "":
    compareWithAllItems()
else:
    compareWithOne(dataset, ownerinput1, ownerinput2)

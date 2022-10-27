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
   dataset[i['user name'].strip()][i['product_name'].strip()] = i['rating']

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

#Function for pearson correlation method
def personCorelation(p1, p2):
    bothRatedThis = {}
    for i in dataset[p1]:
        if i in dataset[p2]:
            bothRatedThis[i] = 1

    numOfRating = len(bothRatedThis)
    if numOfRating == 0:
        return 0

    p1PrefSum = sum([int(dataset[p1][i]) for i in bothRatedThis])
    p2PrefSum = sum([int(dataset[p2][i]) for i in bothRatedThis])

    # Sum the squares of preferences of each user
    p1PrefSquareSum = sum([pow(int(dataset[p1][i]), 2) for i in bothRatedThis])
    p2PrefSquareSum = sum([pow(int(dataset[p2][i]), 2) for i in bothRatedThis])

    # Sum the product value of both preferences for each item
    sumOfBothUsers = sum([int(dataset[p1][i]) * int(dataset[p2][i]) for i in bothRatedThis])

    # Calculate the person score
    numeratorValue = sumOfBothUsers - (p1PrefSum * p2PrefSum / numOfRating)
    denominatorValue = sqrt((p1PrefSquareSum - pow(p1PrefSum, 2) / numOfRating) * (p2PrefSquareSum - pow(p2PrefSum, 2) / numOfRating))

    if denominatorValue == 0.0:
        return 0
    else:
        a = numeratorValue / denominatorValue
        return a

# To find which user is the most similar to the target
def checkSimilarUsers(target, numOfUsers):
    # List comprehension for finding person similarity between users
    scores = [(personCorelation(target,otherPerson), otherPerson) for otherPerson in dataset if otherPerson != target]

    # Sort scores in descending order
    scores.sort(reverse = True)

    # Return scores
    return scores[0:numOfUsers]

# Check similar users to target person
print(checkSimilarUsers('Ellen', 193))

# To see which items users have rated and not rated individually
def seeRatedOrNot(target):
    alist = []
    uList = uniqueItems()
    for i in dataset[target]:
        alist.append(i)

    s = set(uList)
    notRated = list(s.difference(alist))
    a = len(notRated)

    if a == 0:
        return 0
    return notRated, alist

# See which items target user has not rated and rated
'''
nr, r = seeRatedOrNot('Prem')
dct = {"Unrated": nr, "Rated": r}
pd.DataFrame(dct)
print(dct)
'''

def recommendation(target):
    # Gets recommendations for a person by using a weighted average of every other user's rankings
    totals = {}  
    simSums = {} 
    for other in dataset:
        if other == target:
            continue
        sim = personCorelation(target, other)

        # ignore scores of zero or lower
        if sim <= 0:
            continue
        for i in dataset[other]:
            if i not in dataset[target]:
                # Similarity * score
                totals.setdefault(i, 0)
                totals[i] += dataset[other][i] * sim
                # sum of similarities
                simSums.setdefault(i, 0)
                simSums[i] += sim

    rankings = [(total / simSums[i], i) for i, total in totals.items()]
    rankings.sort(reverse=True)

    # Returns the recommended items
    rList = [(i, score) for score, i in rankings]
    return rList

#tp = input("Enter the target person : ")
def init(tp):
    data_dict = {}
    print(dataset.keys())
    if tp in dataset.keys():
        a = recommendation(tp)
        print(a)
        if a != -1:
            print("Recommendation Using User based Collaborative Filtering:  ")
            for i, c in a:
                print(i,'---->', c)
                data_dict[i] = c
        return data_dict

    else:
        print("Person not found in the dataset..please try again")
        return None

#init(tp)
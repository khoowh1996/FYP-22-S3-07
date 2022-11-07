from operator import index, indexOf
from queue import Empty
import pandas as pd
from math import sqrt
import csv
from collections import defaultdict
import pyrebase
import urllib
import io
import base64
import matplotlib.pyplot as plt
import numpy as np


#url = get_database_from_storage()
#webpage = urllib.request.urlopen(url)
# Read the CSV file
#reader = csv.DictReader(io.TextIOWrapper(webpage)) #read from the url
reader = csv.DictReader(open(r'C:\Users\lyhe1\Documents\GitHub\FYP-22-S3-07\algo\Demo.csv'))
#reader = csv.DictReader(open(r'C:\Users\lyhe1\Documents\GitHub\FYP-22-S3-07\algo\Shirts.csv'))
#reader = csv.DictReader(open(r'C:\Users\khoow\OneDrive\Desktop\flask\web1\algo\Demo.csv'))
dataset = defaultdict(dict)

# Put it in a dictionary
for i in reader:
    newI = i['1']
    newnewI = str(newI).replace(newI[0:3], '')
    dataset[newnewI.strip()][i['4'].replace(' ','')] = i['0'].replace(' ','')

# To see the whole dictionary of the data from CSV
print(dataset)


catList = []
ratingList = []
# Get unique set of items bought
def uniqueCategories(dataset):
    uniqueCategoriesList = []
    for p in dataset.keys():
        for i in dataset[p]:
            uniqueCategoriesList.append(i)
    s = set(uniqueCategoriesList)
    uniqueCategoriesList = list(s)
    return uniqueCategoriesList

def compareWithOne(dataset, input1, input2):
    listOfValues = []
    listOfRecommendation = []
    for i in dataset.values():
        # Find who has bought both items that is stated in the arguments
        if input2 in i.keys():
            if input1 in i.keys():
                # Get their values and put all into the list
                if input2 in catList:
                    pass
                else:
                    catList.append(input2)
                listOfValues.append(float(i[input1]))

            if input2 in catList:
                pass
            else:
                catList.append(input2)

    # To handle the exception of division by 0
    if len(listOfValues) == 0:
        listOfRecommendation.append(f'No one has bought, {input1} among people who has bought {input2}')
        ratingList.append(0)
        #print('No one has bought', input1,'among people who has bought',input2)
    else:
        avg = sum(listOfValues) / len(listOfValues)
        ratingList.append(avg)
        if avg <= 2.5:
            listOfRecommendation.append(f'This category of items, {input1} will not do well among people who has bought {input2} as the average rating is {avg}')
            #print('This category of items,', input1, 'will not do well among people who has bought', input2, 'as the average rating is', avg)
        elif avg < 4.0:
            listOfRecommendation.append(f'This category of items, {input1} will be average among people who has bought {input2} as the average rating is {avg}')
            #print('This category of items,', input1, 'will be average among people who has bought', input2, 'as the average rating is', avg)
        elif 4.0 <= avg:
            listOfRecommendation.append(f'This category of items, {input1} will do very well among people who has bought {input2} as the average rating is {avg}')
            #print('This category of items,', input1, 'will do very well among people who has bought', input2, 'as the average rating is', avg)
    listOfValues.clear()
    return listOfRecommendation

def compareWithAllItems(dataset,ownerinput1):
    itemList = uniqueCategories(dataset)
    listOfRecommendation = []
    # Remove the item that the owner wants rating of
    for i in itemList:
        if i == ownerinput1:
            itemList.remove(i)
    # Now compare it to all other items
    for item in itemList:
        recommendations = compareWithOne(dataset, ownerinput1, item)
        for recommendation in recommendations:
            listOfRecommendation.append(recommendation)
    return listOfRecommendation

def get_algorithm_output(url,ownerinput1='highheels',ownerinput2=""):
    try:
        webpage = urllib.request.urlopen(url)
        reader = csv.DictReader(io.TextIOWrapper(webpage))
    except:
        #reader = csv.DictReader(open(r'C:\Users\khoow\OneDrive\Desktop\flask\web1\algo\Demo.csv'))
        # Read the CSV file #read from the url
        reader = csv.DictReader(open(r'C:\Users\lyhe1\Documents\GitHub\FYP-22-S3-07\algo\Demo.csv'))
    dataset = defaultdict(dict)
    listOfRecommendation = []
    # Put it in a dictionary
    for i in reader:
        n = i['1']
        newI = str(n).replace(n[0:3], '')
        dataset[newI.strip()][i['4'].replace(' ','')] = i['0'].replace(' ','')
    if ownerinput2 == "":
        listOfRecommendation = compareWithAllItems(dataset,ownerinput1)
    else:
        listOfRecommendation = compareWithOne(dataset, ownerinput1, ownerinput2)
    return listOfRecommendation,get_graph()

def addLabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

def get_graph():
    plt.bar(catList, ratingList)
    plt.title('Predicted ratings from other categories')
    plt.xlabel('Other categories') 
    plt.ylabel('Average rating')
    addLabels(catList, ratingList)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    #plt.show()
    plt.close()
    return plot_url


ownerinput1 = 'highheels'
ownerinput2 = ''

if ownerinput2 == "":
    compareWithAllItems(dataset,ownerinput1)
else:
    compareWithOne(dataset, ownerinput1, ownerinput2)

# If you want to see it in clearer view
#dd = pd.read_csv(r'C:\Users\lyhe1\Documents\GitHub\FYP-22-S3-07\algo\Demo.csv')
#dd.head()
#dataFrame = pd.DataFrame(dd)
#dataFrame.fillna('No Ratings', inplace = True)
#print(dataFrame)

#ypos = np.arange(len(catList))
#plt.bar(uniqueCategories(dataset), ratingList)
#plt.show()
#print(get_algorithm_output(""))
#get_graph()

plt.bar(catList, ratingList)
plt.title('Predicted ratings from other categories')
plt.xlabel('Other categories')
plt.ylabel('Average rating')
addLabels(catList, ratingList)
plt.show()

print(catList)
print(ratingList)
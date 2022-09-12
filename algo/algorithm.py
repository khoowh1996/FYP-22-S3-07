import pandas as pd
from math import sqrt

# Sample Dataset
dataset = {
    'Lionel': {'Dyson Vacuum Cleaner': 5.0, 
                 'Aftershock PC': 3.0,
                     'Sony Washing Machine': 3.0,
                         'Prism HD TV': 3.0,
                              'Dyson Fan': 2.0,
                                  'HP Laptop': 3.0},
    'Nicholas': {'Dyson Vacuum Cleaner': 5.0, 
                    'Aftershock PC': 3.0,
                        'Sony Washing Machine': 5.0,
                           'Prism HD TV': 5.0,
                               'Dyson Fan': 3.0,
                                   'HP Laptop': 3.0},
    'Jessica': {'Aftershock PC': 2.0,
                    'Dyson Fan': 5.0,
                        'HP Laptop': 3.0,
                            'Prism HD TV': 4.0},
    'WeiHong': {'Prism HD TV': 5.0,
                    'Sony Washing Machine': 4.0,
                        'Dyson Vacuum Cleaner': 4.0},
    'Edwin': {'Dyson Vacuum Cleaner': 4.0,
                'Aftershock PC': 4.0,
                    'Sony Washing Machine': 4.0,
                        'Dyson Fan': 3.0,
                            'HP Laptop': 2.0},
    'Prem': {'Prism HD TV': 3.0,
                'Dyson Vacuum Cleaner': 4.0,
                    'HP Laptop': 3.0,
                        'Sony Washing Machine': 5.0,
                            'Dyson Fan': 3.0},
    'Terence': {'Sony Washing Machine': 4.0,
                    'HP Laptop': 1.0,
                        'Prism HD TV': 4.0}
}

# TO VIEW THE DATASET IN A TABLE AND SET 'NO RATINGS' TO NULL VALUES
dataFrameOfDataSet = pd.DataFrame(dataset)
dataFrameOfDataSet.fillna("No Ratings", inplace = True)
print(dataFrameOfDataSet)

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
# print(uniqueItems())

#Function for pearson correlation method
def personCorelation(p1, p2):
    bothRatedThis = {}
    for i in dataset[p1]:
        if i in dataset[p2]:
            bothRatedThis[i] = 1

    numOfRating = len(bothRatedThis)
    if numOfRating == 0:
        return 0

    p1PrefSum = sum([dataset[p1][i] for i in bothRatedThis])
    p2PrefSum = sum([dataset[p2][i] for i in bothRatedThis])

    # Sum the squares of preferences of each user
    p1PrefSquareSum = sum([pow(dataset[p1][i], 2) for i in bothRatedThis])
    p2PrefSquareSum = sum([pow(dataset[p2][i], 2) for i in bothRatedThis])

    # Sum the product value of both preferences for each item
    sumOfBothUsers = sum([dataset[p1][i] * dataset[p2][i] for i in bothRatedThis])

    # Calculate the person score
    numeratorValue = sumOfBothUsers - (p1PrefSum * p2PrefSum / numOfRating)
    denominatorValue = sqrt((p1PrefSquareSum - pow(p1PrefSum, 2) / numOfRating) * 
    (p2PrefSquareSum - pow(p2PrefSum, 2) / numOfRating))

    if denominatorValue == 0.0:
        return 0
    else:
        a = numeratorValue / denominatorValue
        return a

# To find which user is the most similar to the target
def checkSimilarUsers(target, numOfUsers):
    # List comprehension for finding person similarity between users
    scores = [(personCorelation(target,otherPerson),otherPerson) for otherPerson in dataset if otherPerson != target]

    # Sort scores in descending order
    scores.sort(reverse = True)

    # Return scores
    return scores[0:numOfUsers]

print(checkSimilarUsers('Lionel', 6))

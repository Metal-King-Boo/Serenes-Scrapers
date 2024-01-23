import requests
import pymongo
import json

# grab the URL of the webpage we are scraping
URL = "https://serenesforest.net/binding-blade/classes/base-stats/"
page = requests.get(URL)
# this is a string
fullPage = page.text

splitText = fullPage.split("<tr>")
# 0-71 for this particular page
# pop the first two items which don't have data we want
# the page should now have 0-69 which needs more scraping
splitText.pop(0)
splitText.pop(0)
# pop the intermediate data we don't need
# the page should now have 0-66
splitText.pop(20)
splitText.pop(40)
splitText.pop(60)

# init the three lists needed
nameList = [None] * len(splitText)
statList = [None] * len(splitText)
subList = []

# this loop reads all the titles of the classes in each row
for x in range(len(splitText)):
    titleText = splitText[x]
    titleText = titleText.splitlines()
    titleText = titleText[1].lstrip("<td>")
    titleText = titleText.rstrip("</\td>")
    titleText = titleText.rstrip("t")
    titleText = titleText.rstrip("</")

    # add the names to the big list
    nameList[x] = titleText

# fixing names that have changed with localization
nameList[56] = "Valkyrie"
nameList[57] = "Manakete (M)"
nameList[58] = "Manakete (F)"

# outer loop will run for the whole table
for x in range(len(splitText)):
    # take the first element(list) of the nested list
    statText = splitText[x]
    statText = statText.splitlines()
    # pop the excess data
    statText.pop(0)
    statText.pop(0)

    # this loop creates a list with just the stat values from the table
    for y in range(8):
        subList.append(statText.pop(0))

    # this loop that strips the HTML tags from the data and puts it back into the list
    for y in range(len(subList)):
        test = subList[y].lstrip("<td>")
        test = test.rstrip("</td>")
        subList[y] = test

    # add the list into a bigger list then clear subList
    statList[x] = subList
    subList = []


def send_json_to_mongodb(json_data, collection_name):
    # connect to mongodb
    client = pymongo.MongoClient("mongodb://localhost:27017")

    # select the database
    db = client["FireEmblemData"]

    # select the collection
    collection = db[collection_name]

    # insert the JSON document into the collection
    result = collection.insert_one(json_data)

    print("Document inserted with ID:", result.inserted_id)


# testing space

# create a json with the data given to be sent to a collection
def create_class_json(name, stats, growthList, weapon, unit_type, unit_race):
    created_json = {
        "name": name,
        "type": unit_type,
        "race": unit_race,
        "stage": "Base",
        "base_weapon_ranks": {
            weapon: "D"
        },
        "max_weapon_ranks": {
            weapon: "A"
        },
        "movement": stats[-1],
        "base_stats": {
            "hp": stats[0],
            "str/mag": stats[1],
            "skl": stats[2],
            "spd": stats[3],
            "lck": stats[4],
            "def": stats[5],
            "res": stats[6],
            "con": stats[7]
        },
        "max_stats": {
            "hp": 60,
            "str/mag": 20,
            "skl": 20,
            "spd": 20,
            "lck": 30,
            "def": 20,
            "res": 20,
            "con": 0
        },
        "growth_rates": {
            "hp": 80,
            "str/mag": 40,
            "skl": 40,
            "spd": 32,
            "lck": 30,
            "def": 18,
            "res": 15,
            "con": 0
        }
    }

    return created_json


# collection name and json to be sent
collection_name = "Classes"
growthList = []
send_json = create_class_json(nameList[-2], statList, growthList)

# test cases to know where everything is
print(nameList)
print(statList)

y = 1
k = 1
for x in nameList:
    print(y)
    print(x)
    y += 1

for j in statList:
    print(k)
    print(j)
    k += 1

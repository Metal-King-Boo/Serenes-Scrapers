import requests
import pymongo
import json


def get_data_from_page(site):
    page = requests.get(site)
    page_string = page.text
    split_text = page_string.split("<tr>")
    # 0-71 for this particular page
    # pop the first two items which don't have data we want
    # the page should now have 0-69 which needs more scraping
    split_text.pop(0)
    split_text.pop(0)
    # pop the intermediate data we don't need
    # the page should now have 0-66
    split_text.pop(20)
    split_text.pop(40)
    split_text.pop(60)

    name_list = [None] * len(split_text)
    stat_list = [None] * len(split_text)
    sub_list = []

    # this loop reads all the titles of the classes in each row
    for x in range(len(split_text)):
        title_text = split_text[x]
        title_text = title_text.splitlines()
        title_text = title_text[1].lstrip("<td>")
        title_text = title_text.rstrip("</\td>")
        title_text = title_text.rstrip("t")
        title_text = title_text.rstrip("</")

        # add the names to the big list
        name_list[x] = title_text

    # fixing names that have changed with localization
    name_list[56] = "Valkyrie"
    name_list[57] = "Manakete (M)"
    name_list[58] = "Manakete (F)"

    # outer loop will run for the whole table
    for x in range(len(split_text)):
        # take the first element(list) of the nested list
        stat_text = split_text[x]
        stat_text = stat_text.splitlines()
        # pop the excess data
        stat_text.pop(0)
        stat_text.pop(0)

        # this loop creates a list with just the stat values from the table
        for y in range(8):
            sub_list.append(stat_text.pop(0))

        # this loop that strips the HTML tags from the data and puts it back into the list
        for y in range(len(sub_list)):
            test = sub_list[y].lstrip("<td>")
            test = test.rstrip("</td>")
            sub_list[y] = test

        # add the list into a bigger list then clear subList
        stat_list[x] = sub_list
        sub_list = []

    return name_list, stat_list


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


# create a json with the data given to be sent to a collection
# this version only works for base classes
def create_class_json(name, stats, growths, wpn, unit_type, unit_race):
    created_json = {
        "name": name,
        "type": unit_type,
        "race": unit_race,
        "stage": "Base",
        "base_weapon_ranks": {
            wpn: "D"
        },
        "max_weapon_ranks": {
            wpn: "A"
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
            "con": 20
        },
        "growth_rates": {
            "hp": growths[0],
            "str/mag": growths[1],
            "skl": growths[2],
            "spd": growths[3],
            "lck": growths[6],
            "def": growths[4],
            "res": growths[5],
            "con": 0
        }
    }

    return json.dumps(created_json)


# create a json with the data given to be sent to a collection
# this version only works for advanced classes
def create_adv_class_json(name, stats, max_stats, growths, promos, wpn, wpn2, unit_type, unit_race):
    created_json = {
        "name": name,
        "type": unit_type,
        "race": unit_race,
        "stage": "Advanced",
        "base_weapon_ranks": {
            wpn: "C",
            wpn2: "E"
        },
        "max_weapon_ranks": {
            wpn: "S",
            wpn2: "S"
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
            "str/mag": max_stats[0],
            "skl": max_stats[1],
            "spd": max_stats[2],
            "lck": 30,
            "def": max_stats[3],
            "res": max_stats[4],
            "con": max_stats[5]
        },
        "growth_rates": {
            "hp": growths[0],
            "str/mag": growths[1],
            "skl": growths[2],
            "spd": growths[3],
            "lck": growths[6],
            "def": growths[4],
            "res": growths[5],
            "con": 0
        },
        "promotion_gains": {
            "hp": promos[1],
            "str/mag": promos[2],
            "skl": promos[3],
            "spd": promos[4],
            "lck": 0,
            "def": promos[5],
            "res": promos[6],
            "con": promos[7]
        }
    }

    return json.dumps(created_json)


# URLS and database collection name being used
URL = "https://serenesforest.net/binding-blade/classes/base-stats/"
URL_G = "https://serenesforest.net/binding-blade/classes/growth-rates/"
URL_M = "https://serenesforest.net/binding-blade/classes/maximum-stats/"
URL_P = "https://serenesforest.net/binding-blade/classes/promotion-gains/"
collection_name = "Classes"

# testing information
# growthList will be replaced with the actual growths data
# weapon, unitType, and raceType will be user input
promoList = ["promo", 4, 4, 4, 4, 4, 4, 4, 4, "rank"]
maxList = [25, 25, 25, 25, 25, 25]
weapon = "swords"
weapon2 = "lances"
unitType = "Infantry"
unitRace = "Human"

# call the functions to get the data and create a json
nameList, statList = get_data_from_page(URL)
nameList, growthList = get_data_from_page(URL_G)

#page is significantly shorter so error on pop
#nameList, maxList = get_data_from_page(URL_M)
send_json = create_class_json(nameList[-2], statList[-2], growthList[-2], weapon, unitType, unitRace)
send_json2 = create_adv_class_json(nameList[1], statList[1], maxList, growthList[1], promoList, weapon, weapon2, unitType, unitRace)
# call the function to add the data to the database
# send_json_to_mongodb(send_json, collection_name)

# test cases to know where everything is, its format, and its
#print(nameList)
#print(statList)
#print(growthList2)
print(send_json)
print(send_json2)

# print the data into a files (remove comments when data is updated)
#y = 1
#file = open("binding_blade_table.txt", "w")
#for x in nameList:
#    file.write(str(y) + "\n")
#    file.write(x + "\n")
#    file.write(str(statList[y - 1]) + "\n")
#    y += 1
#file.close()


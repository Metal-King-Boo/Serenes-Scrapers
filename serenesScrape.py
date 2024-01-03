import requests

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

# testing space
print(nameList)
print(statList)

y = 0
for x in nameList:
    print(y)
    print(x)
    y+=1

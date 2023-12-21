import requests

# grab the URL of the webpage we are scraping
URL = "https://serenesforest.net/binding-blade/classes/base-stats/"
page = requests.get(URL)
# this is a string
fullPage = page.text

splitText = fullPage.split("<tr>")
# 0-71 for this particular page
# pop the first two items which don't have data we want
splitText.pop(0)
splitText.pop(0)
# the page should now have 0-69 which needs more scraping

# this path scrapes all the HTML headers from the element
testing = splitText[0]
testing = testing.splitlines()
testing2 = testing[1].lstrip("<td>")
testing3 = testing2.rstrip("</\td>")
testing4 = testing3.rstrip("</t")

# testing the print output for future stripping
print(testing4)
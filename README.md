# Serenes-Scrapers
Mini repository for the scrapers made for pullind information out of the SerenesForest site. This takes the table information and will place them in a MongoDB for use in a future Fire Emblem API. There are plans to use the data for the [true-hit-sim](https://github.com/Metal-King-Boo/true-hit-sim). The current plan is to get most of the data uploads to be automated or at least sped up from manual entry, starting with Binding Blade. When everything is standardized and streamlined I can move to other games with ease and swiftness.

## Directory
### Class Scraper
+ this file has the scraper for the class data used in the database
+ includes base stats, max stats, growth rates, weapon proficiency, and promotion gains.
### Weapon Scraper
+ this file will contain the scraper for the weapon data used in the database
+ includes the might, range, type, effectiveness, accuracy, crit, etc.
### Character Scraper
+ this file will contain the scraper for the character data used in the database
+ includes supports, base stats, level, etc.

## Plan Log (See current stages of development here)
+ finish adding the functions for growth, max data, advanced classes, etc.
+ test the json upload
+ move to characters and weapons

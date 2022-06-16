Quick and dirty script for scraping Microsoft Patching Tuesday .xml file to Excel.
Feel free to customize it for your needs.

.xml File can be downloaded from: https://api.msrc.microsoft.com/cvrf/v2.0/document/2021-Nov


SYNTAX: 

python3 ./<script name> -i <path to .xml file>
(provide path to already downloaded .xml)
or
python3 ./<script name> -r
(GET recent .xml from API endpoint - SUGGESTED)

This script should create a .xlsx file in script's location.

Some sites like https://patchtuesdaydashboard.com/ already provide similar utility, but only for predefined columns. 

play with that script as you like.

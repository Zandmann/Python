Quick and dirty script for scraping Microsoft Patching Tuesday .xml file to Excel.
Feel free to customize it for your needs.

.xml File can be downloaded from: https://api.msrc.microsoft.com/cvrf/v2.0/document/2021-Nov

Just change the "2021-Nov" part accordingly (year and month code) or use Microsoft API.

SYNTAX: python3 ./<script name> -i <path to .xml file>

This should create a .xlsx file in script's location.

Some sites like https://patchtuesdaydashboard.com/ already provide similar utility, but only for predefined columns. 

Here, you can play with that script as you like.

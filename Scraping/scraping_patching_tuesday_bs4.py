#!python3

import requests
from datetime import date
# Import BeautifulSoup
from bs4 import BeautifulSoup as bs
# Import xlsx library
import xlsxwriter
# for parsing arg
import argparse, os
from argparse import ArgumentParser
from os import path
import sys

def validate_file(f):
    if not os.path.exists(f):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(f))
    return f

#get .xml file from API endpoint
def request():
	global xmlfilepath
	today = date.today()
	day = today.strftime("%Y-%b") #date in MS format
	path = 'https://api.msrc.microsoft.com/cvrf/v2.0/document/' + day
	headers = {'User-Agent': 'Gimme that'}
	r = requests.get(path,headers=headers)
	with open(day + '.xml', 'wb') as file:
		file.write(r.content)
		xmlfilepath = day + ".xml"
	return xmlfilepath
	
	
if __name__ == "__main__":


	parser = ArgumentParser(description="Read file form Command line.")
	g = parser.add_mutually_exclusive_group()
	g.add_argument("-i", "--input", dest="filename", type=validate_file,help="path to .xml file", metavar="FILE")
	g.add_argument("-r", "--request", action='store_true',help="make a GET request to MS API endpoint in order to retrieve .xml file")
	args = parser.parse_args()

# Read the XML file
if sys.argv[-1]=="-r" or sys.argv[-1]=="--request":
	request()
	print(xmlfilepath)
	file_path = path.relpath(xmlfilepath)
	with open(file_path) as file:
		bs_content = bs(file, "html.parser")
		
if sys.argv[-2]=="-i" or sys.argv[-2]=="--input":
	file_path = path.relpath(args.filename)
	with open(file_path) as file:
		bs_content = bs(file, "html.parser")
	


# Create an new Excel file and add a worksheet.
workbook = xlsxwriter.Workbook('vulnerabilities_list.xlsx')
worksheet = workbook.add_worksheet()
worksheet2 = workbook.add_worksheet()

#worksheet set column width table1
bold   = workbook.add_format({'bold': True, 'align': 'center', 'border': 2})
center = workbook.add_format({'align': 'center', 'border': 2})
blank = workbook.add_format({'align': 'center'})
worksheet.set_column(0,0, 15,center)
worksheet.set_column(1,1, 65,center)
worksheet.set_column(2,2, 15,center)
worksheet.set_column(3,3, 25,center)
worksheet.set_column(4,4, 15,center)
worksheet.set_column(5,5, 15,center)
worksheet.set_column(6,6, 20,center)
worksheet.set_column(7,7, 30,center)
worksheet.set_column(8,8, 60,center)
worksheet.set_column(9,9, 60,center)

#worksheet2 set column width table2
worksheet2.set_column(0,0, 30,bold)
worksheet2.set_column(1,1, 70,center)

#worksheet column names
worksheet.write(0, 0, "CVE", bold)
worksheet.write(0, 1, "Product Family", bold)
worksheet.write(0, 2, "Microsoft Severity", bold)
worksheet.write(0, 3, "Maximum Impact", bold)
worksheet.write(0, 4, "CVSS Score", bold)
worksheet.write(0, 5, "Publicly Disclosed", bold)
worksheet.write(0, 6, "Known Exploits", bold)
worksheet.write(0, 7, "Exploitability Assessment Latest", bold)
worksheet.write(0, 8, "Affected Software", bold)
worksheet.write(0, 9, "More Details", bold)

#dictionary population
product_tree = bs_content.find('prod:producttree').find_all('prod:fullproductname')

products_IDs = []
products_names = []

for productid in product_tree:
	product_id = productid.get('productid')
	products_IDs.append(product_id)
	
for productname in product_tree:
	product_name = productname.text
	products_names.append(product_name)
	
product_dictionary = dict(zip(products_IDs, products_names))

#vulnerabilities iteration
vuln_titles = []
vulns = bs_content.find_all('vuln:vulnerability')
index = 1
index2 = 1
for vuln in vulns:
	try:
		title = vuln.find('vuln:title')
	except AttributeError:
		title = None
	try:
		cve = vuln.find('vuln:cve')
	except AttributeError:
		cve = None
	try:
		affected = vuln.find('vuln:status',type="Known Affected")
	except AttributeError:
		affected = None
	try:
		threat_impact = vuln.find('vuln:threats').find('vuln:threat',type="Impact").find('vuln:description')
	except AttributeError:
		threat_impact = None
	try:
		threat_severity = vuln.find('vuln:threats').find('vuln:threat',type="Severity").find('vuln:description')
	except AttributeError:
		threat_severity = None
	try:
		threat_exploit = vuln.find('vuln:threats').find('vuln:threat',type="Exploit Status").find('vuln:description')
	except AttributeError:
		threat_exploit = None
	try:
		publicly_disclosed = threat_exploit.text.split(";")[0].split(":")[1]
	except AttributeError:
		publicly_disclosed = None
	except IndexError:
		publicly_disclosed = None
	try:
		exploited = threat_exploit.text.split(";")[1].split(":")[1]
	except AttributeError:
		exploited = None
	except IndexError:
		exploited = None
	try:
		exploit_assessment_latest = threat_exploit.text.split(";")[2].split(":")[1]
	except AttributeError:
		exploit_assessment_latest = None
	except IndexError:
		exploit_assessment_latest = None
	try:
		cvss_score = vuln.find('vuln:cvssscoresets').find('vuln:scoreset').find('vuln:basescore')
	except AttributeError:
		cvss_score = None
	try:
		cvss_vector_all = vuln.find('vuln:cvssscoresets').find('vuln:scoreset').find('vuln:vector')
	except AttributeError:
		cvss_vector_all = None
	try:
		cvss_vector_AV = cvss_vector_all.text.split("/")[1].split(":")[1]				
	except AttributeError:
		cvss_vector_AV = None
	except IndexError:
		cvss_vector_AV = None

	vuln_titles.append(title.text)
	
	print(title.text,"\n")
	if affected != None:
		for aff in affected:
			print(product_dictionary[aff.text])
			
	print("\n", "--------------------------------------")

	#make color formats for code red,yellow,green	
	format_red = workbook.add_format({'bg_color': '#FF0000', 'align': 'center', 'border': 2})
	format_yellow = workbook.add_format({'bg_color': '#FFFF00', 'align': 'center', 'border': 2})
	format_green = workbook.add_format({'bg_color': '#92D050', 'align': 'center', 'border': 2})
	format_orange = workbook.add_format({'bg_color': '#FFC000', 'align': 'center', 'border': 2})

	font_green = workbook.add_format({'font_color': '#92D050', 'align': 'center', 'border': 2})
	font_orange = workbook.add_format({'font_color': '#FFC000', 'align': 'center', 'border': 2})
	font_red = workbook.add_format({'font_color': '#FF0000', 'align': 'center', 'border': 2})

	#write to worksheet, row by index - table1
	
	if cve != None:
		worksheet.write(index, 0, cve.text)
	
	if title != None:
		worksheet.write(index, 1, title.text)
	
	if threat_severity != None:
		if threat_severity.text == "Important":
			worksheet.write(index, 2, threat_severity.text, font_orange)
		elif threat_severity.text == "Critical":
			worksheet.write(index, 2, threat_severity.text, font_red)
		else:
			worksheet.write(index, 2, threat_severity.text, font_green)
			
	if threat_impact != None:
		worksheet.write(index, 3, threat_impact.text)
	
	if cvss_score != None:
		if float(cvss_score.text) >= 9.0:
			worksheet.write(index, 4, cvss_score.text,format_red)
		elif 5.0 < float(cvss_score.text) < 9.0:
			worksheet.write(index, 4, cvss_score.text,format_yellow)
		else:
			worksheet.write(index, 4, cvss_score.text,format_green)
			
	if publicly_disclosed != None:
		if publicly_disclosed == "Yes":
			worksheet.write(index, 5, publicly_disclosed, format_red)
		else:
			worksheet.write(index, 5, publicly_disclosed, format_green)
	
	if exploited != None:
		if exploited == "Yes":
			worksheet.write(index, 6, exploited, format_red)
		else:
			worksheet.write(index, 6, exploited, format_green)
			
	if exploit_assessment_latest != None:	
		if exploit_assessment_latest == "Exploitation More Likely":
			worksheet.write(index, 7, exploit_assessment_latest, format_orange)
		elif exploit_assessment_latest == "Exploitation Detected":
			worksheet.write(index, 7, exploit_assessment_latest, format_red)
		else:
			worksheet.write(index, 7, exploit_assessment_latest, format_green)
	
	affected_products = []
	
	if affected != None:
		for aff in affected:
			affected_products.append(product_dictionary[aff.text])
		worksheet.write(index, 8, '\n'.join(affected_products))
	if cve != None:
		worksheet.write(index, 9, f"https://msrc.microsoft.com/update-guide/vulnerability/{cve.text}")

	#increment index for table1 by 1 so another row will be populated on next loop
	index += 1

	#worksheet2 row names
	worksheet2.write(index2+1, 0, "Affected Software", bold)
	worksheet2.write(index2+2, 0, "Impact", bold)
	worksheet2.write(index2+3, 0, "Severity", bold)
	worksheet2.write(index2+4, 0, "Publicly Disclosed?", bold)
	worksheet2.write(index2+5, 0, "Known Exploits?", bold)
	worksheet2.write(index2+6, 0, "Exploitability Assessment Latest", bold)
	worksheet2.write(index2+7, 0, "CVSS Score", bold)
	worksheet2.write(index2+8, 0, "More Details", bold)
	worksheet2.write(index2+9, 0, "", blank)

	#write to worksheet, row by index - table2
	worksheet2.write(index2, 0, cve.text, bold)
	worksheet2.write(index2, 1, title.text)
	
	if threat_severity != None:
		if threat_severity.text == "Important":
			worksheet2.write(index2+3, 1, threat_severity.text, format_orange)
		elif threat_severity.text == "Critical":
			worksheet2.write(index2+3, 1, threat_severity.text, format_red)
		else:
			worksheet2.write(index2+3, 1, threat_severity.text, format_green)
		
	if cvss_score != None:
		if float(cvss_score.text) >= 9.0:
			worksheet2.write(index2+7, 1, f"{cvss_score.text} - RED",format_red)
		elif 5.0 < float(cvss_score.text) < 9.0:
			worksheet2.write(index2+7, 1, f"{cvss_score.text} - YELLOW",format_yellow)
		else:
			worksheet2.write(index2+7, 1, f"{cvss_score.text} - GREEN",format_green)
			
	if threat_impact != None:
		worksheet2.write(index2+2, 1, threat_impact.text, center)
	#worksheet2.write(index2, 5, cvss_score.text)
	
	if publicly_disclosed != None:
		if publicly_disclosed == "Yes":
			worksheet2.write(index2+4, 1, publicly_disclosed, format_red)
		else:
			worksheet2.write(index2+4, 1, publicly_disclosed, format_green)
			
	if exploited != None:
		if exploited == "Yes":
			worksheet2.write(index2+5, 1, exploited, format_red)
		else:
			worksheet2.write(index2+5, 1, exploited, format_green)
			
	if exploit_assessment_latest != None:	
		if exploit_assessment_latest == "Exploitation More Likely":
			worksheet2.write(index2+6, 1, exploit_assessment_latest, format_orange)
		elif exploit_assessment_latest == "Exploitation Detected":
			worksheet2.write(index2+6, 1, exploit_assessment_latest, format_red)
		else:
			worksheet2.write(index2+6, 1, exploit_assessment_latest, format_green)
			
	if affected_products != None:
		worksheet2.write(index2+1, 1, '\n'.join(affected_products))
	if cve != None:
		worksheet2.write(index2+8, 1, f"https://msrc.microsoft.com/update-guide/vulnerability/{cve.text}", center)
	worksheet2.write(index2+9, 1, "", blank)

	#increment index for table2 by 9 so another distant row will be populated on next loop
	index2 += 10

workbook.close()
print("vulnerabilities count: {}".format(len(vuln_titles)))



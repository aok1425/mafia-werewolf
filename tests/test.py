#!/Users/ako/anaconda/bin/python

import requests
import random
import time

players = {
	"Villager": ["v1", "v2", "v3", "v4", "v5", "v6", "v7"],
	"Mafia": ["m1", "m2", "m3", "m4"],
	"Sheriff": ["s1", "s2", "s3"],
	"Angel": ["a1", "a2"],
	"Doesn't Matter": ["d1", "d2"]}

for role in players:
	for name in players[role]:
		# print "http://127.0.0.1:5000/test_login/{}/{}/test".format(name, role)
		requests.get("http://127.0.0.1:5000/test_login/{}/{}/test".format(name, role))
		# time.sleep(1)
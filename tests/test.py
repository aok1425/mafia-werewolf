import requests
import random
import time

number_players = {
	"Villager": 2,
	"Mafia": 4,
	"Sheriff": 3,
	"Angel": 0,
	"Doesn't Matter": 7}

players = {}

# making the player names
for role in number_players:
	if not role in players:
		players[role] = []
	for i in range(1, number_players[role] + 1):
		players[role].append(role[0].lower() + str(i))

def create_players(players, url="127.0.0.1:5000"):
	for role in players:
		for name in players[role]:
			print "http://{}/test_login/{}/{}/test".format(url, name, role)
			requests.get("http://{}/test_login/{}/{}/test".format(url, name, role))
			# time.sleep(1)

if __name__=="__main__":
	create_players(players)
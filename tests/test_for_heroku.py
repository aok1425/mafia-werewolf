from test import create_players

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

create_players(players, url="mafiaalex.herokuapp.com")
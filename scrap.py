import random
from time import sleep
from math import ceil

names = ['Jane', 'Jack', 'Molly', 'Alex', 'Nico', 'Nostradamus', 'Dave', 'Laurie']

for name in [names[1]]:
	c.execute('''INSERT INTO players(date_time, name) VALUES(?, ?)''', (1417184219, name))
	print unix_time(datetime.datetime.now())
	sleep(1)

db.commit()

c.execute('''SELECT * FROM players''')
c.fetchall()

c.execute('''SELECT * FROM players''')
players = c.fetchall()

num_mafia = int(ceil(len(players)/3.))

if len(players) > 6:
	chosen_player = random.randint(0, len(players) - 1)
	chosen_player_id = players.pop(chosen_player)[0]
	c.execute("update players set role = 'Sheriff' where date_time = {}".format(chosen_player_id))

if len(players) > 7:
	chosen_player = random.randint(0, len(players) - 1)
	chosen_player_id = players.pop(chosen_player)[0]
	c.execute("update players set role = 'Angel' where date_time = {}".format(chosen_player_id))

for i in range(num_mafia):
	chosen_player = random.randint(0, len(players) - 1)
	chosen_player_id = players.pop(chosen_player)[0]
	c.execute("update players set role = 'Mafia' where date_time = {}".format(chosen_player_id))

for i in [row[0] for row in players]:
	c.execute("update players set role = 'Villager' where date_time = {}".format(i))

db.commit()

c.execute('''SELECT * FROM players''')
c.fetchall()

c.execute('''SELECT role FROM players WHERE date_time = ?''', (1417184341,))
c.fetchone()[0]
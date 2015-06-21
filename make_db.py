import sqlite3

db = sqlite3.connect("main.db")
c = db.cursor()

c.execute('''DROP TABLE IF EXISTS players''')
db.commit()

c.execute('''CREATE TABLE players(date_time integer, name TEXT, role TEXT, preferred_role TEXT, game TEXT, PRIMARY KEY (date_time, name))''')
db.commit()

c.execute('''DROP TABLE IF EXISTS games''')
db.commit()

c.execute('''CREATE TABLE games(date_time integer, game TEXT, phone_number integer, PRIMARY KEY (date_time, game))''')
db.commit()

db.close()
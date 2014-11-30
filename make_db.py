import sqlite3

db = sqlite3.connect("main.db")
c = db.cursor()

c.execute('''DROP TABLE IF EXISTS players''')
db.commit()

c.execute('''CREATE TABLE players(date_time integer, name TEXT, role TEXT, preferred_role TEXT, PRIMARY KEY (date_time, name))''')
db.commit()

db.close()
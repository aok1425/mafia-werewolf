import sqlite3

db = sqlite3.connect("test.db")
c = db.cursor()
c.execute('''DROP TABLE IF EXISTS players''')
db.commit()


c.execute('''CREATE TABLE players(date_time timestamp default (strftime('%s', 'now')) PRIMARY KEY, name TEXT, role TEXT)''')
db.commit()
"""
# Insert a date object into the database
c.execute('''INSERT INTO players(name) VALUES(?)''', ('Jane',))
db.commit()

# Retrieve the inserted object
c.execute('''SELECT * FROM players''')
c.fetchall()

c.execute('''SELECT * FROM players WHERE date_time >= (strftime('%s', 'now') - 5 * 60)''')
c.fetchall()
"""
db.close()
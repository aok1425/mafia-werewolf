from flask import Flask, session, redirect, url_for, escape, request
import sqlite3
from math import ceil
import random
from time import sleep

app = Flask(__name__)
db = sqlite3.connect("test.db", check_same_thread=False)
c = db.cursor()

def assign_roles(database):
    """Takes in a database result, chooses roles for each player, and updates the db."""
    num_mafia = int(ceil(len(database)/3.))

    if len(database) > 6:
        chosen_player = random.randint(0, len(database) - 1)
        chosen_player_id = database.pop(chosen_player)[0]
        c.execute("update players set role = 'Sheriff' where date_time = {}".format(chosen_player_id))

    if len(database) > 7: # bc of the pop
        chosen_player = random.randint(0, len(database) - 1)
        chosen_player_id = database.pop(chosen_player)[0]
        c.execute("update players set role = 'Angel' where date_time = {}".format(chosen_player_id))

    for i in range(num_mafia):
        chosen_player = random.randint(0, len(database) - 1)
        chosen_player_id = database.pop(chosen_player)[0]
        c.execute("update players set role = 'Mafia' where date_time = {}".format(chosen_player_id))

    for i in [row[0] for row in database]:
        c.execute("update players set role = 'Villager' where date_time = {}".format(i))

    db.commit()

@app.route('/')
def index():
    if 'username' in session:
        c.execute('''SELECT * FROM players WHERE date_time >= (strftime('%s', 'now') - 5 * 600)''')
        players = c.fetchall()
        return 'Logged in as {}. The other players are: {}'.format(escape(session['username']), str(players))
    return 'You are not logged in'

@app.route('/host', methods=['GET', 'POST'])
def host():
    c.execute('''SELECT * FROM players WHERE date_time >= (strftime('%s', 'now') - 5 * 600)''')
    players = c.fetchall()

    if request.method == 'POST':
        assign_roles(players)

        c.execute('''SELECT * FROM players WHERE date_time >= (strftime('%s', 'now') - 5 * 600)''')
        players = c.fetchall()
        
        return '''These are the roles of the players. \n {}'''.format(str(players))
    else:
        return '''
            These are the players:{}.
            <form action="" method="post">
                <p>Press submit, and the computer will assign players their roles.
                <p><input type=submit value=Submit>
            </form>
        '''.format(str(players))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        c.execute('''INSERT INTO players(name) VALUES(?)''', (request.form['username'],))
        db.commit()
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'alex'

if __name__ == '__main__':
    app.run(debug=True)
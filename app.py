from flask import Flask, session, redirect, url_for, escape, request, render_template
import sqlite3
import random
import datetime
from math import ceil

app = Flask(__name__)
db = sqlite3.connect("test.db", check_same_thread=False)
c = db.cursor()

app.permanent_session_lifetime = 60 * 5 # seconds

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return int(delta.total_seconds())

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
        c.execute('''SELECT * FROM players WHERE date_time >= ?''', (unix_time(datetime.datetime.now()) - 5 * 60,))
        players = c.fetchall()
        return render_template('player_waiting.html', players=players, name=session['username'])
    return redirect(url_for('login'))

@app.route('/role', methods=['GET', 'POST'])
def role():
    if request.method == 'POST':
        session['date_time'] = unix_time(datetime.datetime.now())
        c.execute('''INSERT INTO players(date_time, name) VALUES(?, ?)''', (session['date_time'], session['username']))
        db.commit()
        return redirect(url_for('index'))
    if 'username' in session:
        c.execute('''SELECT role FROM players WHERE date_time = ?''', (session['date_time'],))
        session['role'] = c.fetchone()[0]
        return render_template('player_role.html', name=session['username'], role=session['role'])
    return redirect(url_for('login'))

@app.route('/host', methods=['GET', 'POST'])
def host():
    if request.method == 'POST':
        c.execute('''SELECT * FROM players WHERE {}'''.format('date_time = ' + ' OR date_time = '.join(request.form.values())))
        players = c.fetchall()    
            
        assign_roles(players)

        c.execute('''SELECT * FROM players WHERE {} ORDER BY role'''.format('date_time = ' + ' OR date_time = '.join(request.form.values())))
        players = c.fetchall()
        #return '{}'.format(str(request.form))
        return render_template('host_after.html', players=players)
    else:
        c.execute('''SELECT * FROM players WHERE date_time >= ?''', (unix_time(datetime.datetime.now()) - 5 * 60,))
        players = c.fetchall()
        return render_template('host_before.html', players=players)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['date_time'] = unix_time(datetime.datetime.now())
        c.execute('''INSERT INTO players(date_time, name) VALUES(?, ?)''', (session['date_time'], session['username']))
        db.commit()
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'alex'

if __name__ == '__main__':
    app.run(debug=True)
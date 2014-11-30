from flask import Flask, session, redirect, url_for, escape, request, render_template
import sqlite3
import random
import datetime
from math import ceil

app = Flask(__name__)
db = sqlite3.connect("main.db", check_same_thread=False)
c = db.cursor()

app.permanent_session_lifetime = 60 * 5 # seconds

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return int(delta.total_seconds())

# revise this to update based on name AND date_time, not just the latter
def assign_roles(database, num_mafia, num_sheriff, num_angel):
    """Takes in a database result, chooses roles for each player, and updates the db."""
    num_players = len(database)
    num_villagers = num_players - num_mafia - num_sheriff - num_angel

    num_assigned_sheriff = 0
    num_assigned_angel = 0
    num_assigned_mafia = 0
    num_assigned_villagers = 0

    for num, row in enumerate(database): # to make random, shuffle tuples
        if num_assigned_sheriff < num_sheriff:
            if row[-1] == 'Sheriff':
                chosen_player_id = database.pop(num)[0]
                c.execute("update players set role = 'Sheriff' where date_time = {}".format(chosen_player_id))
                num_assigned_sheriff += 1
        if num_assigned_angel < num_angel:
            if row[-1] == 'Angel':
                chosen_player_id = database.pop(num)[0]
                c.execute("update players set role = 'Angel' where date_time = {}".format(chosen_player_id))
                num_assigned_angel += 1
        if num_assigned_mafia < num_mafia:
            if row[-1] == 'Mafia':
                chosen_player_id = database.pop(num)[0]
                c.execute("update players set role = 'Mafia' where date_time = {}".format(chosen_player_id))
                num_assigned_mafia += 1
        if num_assigned_villagers < num_villagers:
            if row[-1] == 'Villager':
                chosen_player_id = database.pop(num)[0]
                c.execute("update players set role = 'Villager' where date_time = {}".format(chosen_player_id))
                num_assigned_villagers += 1

    for i in range(num_mafia - num_assigned_mafia):
        chosen_player = random.randint(0, len(database) - 1)
        chosen_player_values = database.pop(chosen_player)
        chosen_player_id = chosen_player_values[0]
        chosen_player_name = chosen_player_values[1]
        c.execute("update players set role = 'Mafia' where date_time = {} and name = '{}'".format(chosen_player_id, chosen_player_name))

    for i in range(num_sheriff - num_assigned_sheriff):
        chosen_player = random.randint(0, len(database) - 1)
        chosen_player_values = database.pop(chosen_player)
        chosen_player_id = chosen_player_values[0]
        chosen_player_name = chosen_player_values[1]
        c.execute("update players set role = 'Sheriff' where date_time = {} and name = '{}'".format(chosen_player_id, chosen_player_name))

    for i in range(num_angel - num_assigned_angel):
        chosen_player = random.randint(0, len(database) - 1)
        chosen_player_values = database.pop(chosen_player)
        chosen_player_id = chosen_player_values[0]
        chosen_player_name = chosen_player_values[1]
        c.execute("update players set role = 'Angel' where date_time = {} and name = '{}'".format(chosen_player_id, chosen_player_name))

    for chosen_player_id, chosen_player_name in [row[:2] for row in database]:
        c.execute("update players set role = 'Villager' where date_time = {} and name = '{}'".format(chosen_player_id, chosen_player_name))

    db.commit()

@app.route('/')
def index():
    if 'username' in session:
        c.execute('''SELECT * FROM players WHERE date_time >= ?''', (unix_time(datetime.datetime.now()) - 5 * 60,))
        players = c.fetchall()

        return render_template('player_waiting.html', players=players, name=session['username'], num=len(players))
    return redirect(url_for('login'))

@app.route('/role', methods=['GET', 'POST'])
def role():
    if request.method == 'POST':
        session['date_time'] = unix_time(datetime.datetime.now())
        c.execute('''INSERT INTO players(date_time, name) VALUES(?, ?)''', (session['date_time'], session['username']))
        db.commit()
        return redirect(url_for('index'))
    if 'username' in session:
        c.execute('''SELECT role FROM players WHERE date_time = ? AND name = ?''', (session['date_time'], session['username']))
        session['role'] = c.fetchone()[0]
        return render_template('player_role.html', name=session['username'], role=session['role'])
    return redirect(url_for('login'))

@app.route('/host', methods=['GET', 'POST'])
def host():
    if request.method == 'POST':
        #return str(request.form['mafia']) + str(request.form['sheriff']) + str(request.form['angel'])

        c.execute('''SELECT * FROM players WHERE {}'''.format('date_time = ' + ' OR date_time = '.join(request.form.values())))
        players = c.fetchall()    
            
        assign_roles(players, int(request.form['mafia']), int(request.form['sheriff']), int(request.form['angel']))

        c.execute('''SELECT * FROM players WHERE {} ORDER BY role'''.format('date_time = ' + ' OR date_time = '.join(request.form.values())))
        players = c.fetchall()

        players = [[num]+list(values) for num, values in list(enumerate(players, 1))]
        
        return render_template('host_after.html', players=players)
    else:
        c.execute('''SELECT * FROM players WHERE date_time >= ?''', (unix_time(datetime.datetime.now()) - 5 * 60,))
        players = c.fetchall()

        num_players = len(players)
        num_mafia = [int(num_players/3.), int(ceil(num_players/3.))]

        if num_mafia[0] == num_mafia[1]:
            num_mafia[0] -= 1

        if num_players > 6 and num_players < 12:
            num_sheriff = [0,1]
            num_angel = [0,1]
        elif num_players >= 12:
            num_sheriff = [1,2]
            num_angel = [1,2]
        else:
            num_sheriff = [0,1]
            num_angel = [0,1]

        return render_template('host_before.html', players=players, num_mafia=num_mafia, num_sheriff=num_sheriff, num_angel=num_angel, num_players=num_players)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #return str(request.form)
        session['username'] = request.form['username']
        session['date_time'] = unix_time(datetime.datetime.now())
        c.execute('''INSERT INTO players(date_time, name, preferred_role) VALUES(?,?,?)''', (session['date_time'], session['username'], request.form['preferred_role']))
        db.commit()
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/login/<string:name>', methods=['GET'])
def login_w_name(name):
    session['username'] = name
    session['date_time'] = unix_time(datetime.datetime.now())
    c.execute('''INSERT INTO players(date_time, name) VALUES(?, ?)''', (session['date_time'], session['username']))
    db.commit()
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'alex'

if __name__ == '__main__':
    app.run(debug=True)
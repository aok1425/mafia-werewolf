def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return int(delta.total_seconds())

def assign_roles(database, num_mafia, num_sheriff, num_angel, columns):
    """Takes in a database result, shuffles rows, chooses roles for each player, and updates the db."""
    counters = {}
    counters['Villager'] = [len(database) - num_mafia - num_sheriff - num_angel, 0]
    counters['Mafia'] = [num_mafia, 0]
    counters['Sheriff'] = [num_sheriff, 0]
    counters['Angel'] = [num_angel, 0]

    random.shuffle(database)

    for num, row in enumerate(database): # assign requested roles
        for role in counters.keys():
            if counters[role][columns.index('name')] < counters[role][columns.index('date_time')]:
                if row[columns.index('preferred_role')] == role:
                    row = database.pop(num)
                    date_time, name = row[:2]
                    c.execute("update players set role = '{}' where date_time = {} and name = '{}'".format(role, date_time, name))
                    counters[role][c.index('name')] += 1

    for role in counters.keys(): # randomly assign rest of roles
        for i in range(counters[role][columns.index('date_time')] - counters[role][columns.index('name')]):
            chosen_player = random.randint(0, len(database) - 1)
            row = database.pop(chosen_player)
            date_time, name = row[:2]
            c.execute("update players set role = '{}' where date_time = {} and name = '{}'".format(role, date_time, name))

    db.commit()
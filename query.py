import discord
from main import db


'''
Remember to call db.commit() after executing queries to save them
Exiting a function may NOT delete a cursor, call cursor.close() instead
'''


# Creates client in database if client there is none
def set_clientid(client: discord.User) -> str:
    c_id = str(client.id)
    c_name = client.name
    cursor = db.cursor()
    cursor.execute(f'select clientid from client where clientid = {c_id}')
    r = cursor.fetchone()
    # Checks for c_id in client table
    if r is None:
        cursor.execute(f'insert into client (clientid, clientname) values ("{c_id}", "{c_name}")')
        db.commit()
    cursor.close()
    return c_id


# Returns the technician who currently has the least amount of work
def get_techid() -> str:
    # TODO: convert this logic into a sql query
    # Assigns a numeric value to each severity level
    severity = {'High': 5, 'Medium': 3, 'Low': 1}
    cursor = db.cursor()
    cursor.execute('select techid from tech where techactive = 1')
    # techs and workloads are parallel lists where the workloads of the technician at techs[i] is workloads[i]
    techs = cursor.fetchall()
    workloads = []
    for i in range(len(techs)):
        workloads.append(0)
        t = techs[i][0]
        cursor.execute(f'select ticketseverity from ticket where tickettech = {t}')
        r = cursor.fetchall()
        if len(r) > 0:
            for j in r:
                workloads[i] += severity.get(j[0])
    cursor.close()
    # Assigns t to the technician at the same index of the maximum value in workloads
    t = techs[workloads.index(max(workloads))][0]
    return t


# Creates new ticket
def create_ticket(client: discord.User, t_id: str, subject: str, description: str, severity: str) -> None:
    c_id = set_clientid(client)
    cursor = db.cursor()
    cursor.execute(
        f'insert into ticket (ticketclient, tickettech, ticketopendate, tickettitle, ticketdescription, ticketseverity)'
        f'values ({c_id}, {t_id}, CURDATE(), "{subject}", "{description}", "{severity}")')
    db.commit()
    cursor.close()


# Gets the senior technician id
def get_mgr() -> str | None:
    cursor = db.cursor()
    cursor.execute(f'select techid from tech where techrank = "Senior"')
    r = cursor.fetchone()[0]
    cursor.close()
    return r


# Creates a new technician
def create_tech(tech: discord.Member, rank: str = 'Junior', mgr: str = None) -> None:
    t_id = tech.id
    t_name = tech.name
    cursor = db.cursor()
    cursor.execute(f'select techid from tech where techid = {t_id}')
    # Checks if tech is already in database
    if cursor.fetchone():
        cursor.execute(f'update tech set techactive = 1 where techid = {t_id}')
    # Creates new tech in database
    else:
        if rank == 'Junior' and mgr is None:
            mgr = get_mgr()
        cursor.execute(f'insert into tech (techid, techname, techrank, techmgr) values ({t_id}, "{t_name}", "{rank}", {mgr})')
    db.commit()
    cursor.close()


# Sets a technician to inactive in the database
def remove_tech(tech: discord.Member) -> None:
    t_id = tech.id
    cursor = db.cursor()
    cursor.execute(f'update tech set techactive = 0 where techid = {t_id}')
    db.commit()
    cursor.close()

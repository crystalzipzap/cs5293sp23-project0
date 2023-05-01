import sqlite3

def createdb():   
    connect = sqlite3.connect('normanpd.db')
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS incidents
                (incident_time TEXT,
                incident_number TEXT,
                incident_location TEXT,
                nature TEXT,
                incident_ori TEXT);''')
    connect.commit()
    return connect

def populatedb(incidents_list):
    connect = sqlite3.connect('normanpd.db')
    cursor = connect.cursor()
    for incident in incidents_list:
        cursor.execute("INSERT INTO incidents VALUES (?, ?, ?, ?, ?)", 
                       (incident.time, incident.number, incident.location, incident.nature, incident.ori))
        connect.commit()
    connect.close()

def status():
    connect = sqlite3.connect('normanpd.db')
    cursor = connect.cursor()
    cursor.execute("SELECT nature, COUNT(*) FROM incidents WHERE nature != '' GROUP BY nature")
    for line in cursor:
        print(f'{line[0]}|{line[1]}')
    connect.close()
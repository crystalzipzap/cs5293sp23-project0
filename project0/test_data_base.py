import os
import pytest
import sqlite3
from incident import Incident
from database import createdb, populatedb, status

@pytest.fixture(scope='module')
def incidents():
    incidents_list = [Incident('3/1/2023 0:06', '2023-00013135', '201 W GARY ST', 'Follow Up', 'OK0140200'),
                      Incident('3/1/2023 1:21', '2023-00003099', '5150 175TH AVE NE', 'Falls', '14005'),
                      Incident('3/1/2023 1:21', '2023-00004072', '5150 175TH AVE NE', 'Falls', 'EMSSTAT'),
                      Incident('3/1/2023 1:25', '2023-00013148', '631 CLASSEN BLVD', 'Traffic Stop', 'OK0140200')]
    return incidents_list

@pytest.fixture(autouse=True)
def delete_database():
    # delete database file if it exists
    if os.path.exists("normanpd.db"):
        os.remove("normanpd.db")

def test_createdb():
    connection = createdb()
    assert isinstance(connection, sqlite3.Connection)
    connection.close()

def test_populatedb(incidents):
    connection = createdb()
    populatedb(incidents)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM incidents")
    result = cursor.fetchone()
    assert result[0] == len(incidents)
    connection.close()

def test_status(incidents, capsys):
    connection = createdb()
    populatedb(incidents)
    status()
    out, _ = capsys.readouterr()
    assert "Falls|2\nFollow Up|1\nTraffic Stop|1\n" in out
    connection.close()
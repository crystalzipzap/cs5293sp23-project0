import pytest
from incident import Incident
def test_incident():
    incident1 = Incident('3/1/2023 0:06', '2023-00013135', '201 W GARY ST', 'Follow Up', 'OK0140200')
    assert incident1.location == '201 W GARY ST'
    assert incident1.nature == 'Follow Up'
    
    
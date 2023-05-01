import os
import pytest
import re
import urllib.request
from pypdf import PdfReader
from file_extraction import file_path_generator, fetch_incidents, extract_incidents
from incident import Incident


def test_file_path_generator():
    url1 = 'https://www.normanok.gov/sites/default/files/documents/2023-03/2023-03-01_daily_incident_summary.pdf'
    expected1 = '2023-03-01_daily_incident_summary.pdf'
    assert file_path_generator(url1) == expected1

    url2 = 'https://www.normanok.gov/sites/default/files/documents/2023-03/2023-03-15_daily_incident_summary.pdf'
    expected2 = '2023-03-15_daily_incident_summary.pdf'
    assert file_path_generator(url2) == expected2
    
    url3 = 'https://www.normanok.gov/sites/default/files/documents/2023-04/2023-03-31_daily_incident_summary.pdf'
    expected3 = '2023-03-31_daily_incident_summary.pdf'
    assert file_path_generator(url3) == expected3
    
def test_fetch_incidents(tmp_path):
    file_path = 'project0/2023-03-01_daily_incident_summary.pdf'
    assert os.path.exists(file_path)
                                         
def test_extract_incidents():
    file_path = 'project0/2023-03-01_daily_incident_summary.pdf'
    incidents = extract_incidents(file_path)
    assert isinstance(incidents[0], Incident)


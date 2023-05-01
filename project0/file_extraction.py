import os
import urllib.request
from pypdf import PdfReader
import re
from incident import Incident

def file_path_generator(url):
    file_name_pattern = r'\d{4}-\d{2}-\d{2}_.*\.pdf'
    result = re.search(file_name_pattern, url)
    file_name = result.group(0)
    os.makedirs('docs', exist_ok=True)
    return f'docs/{file_name}'

def fetch_incidents(url):
    file_path = file_path_generator(url)
    if not os.path.exists(file_path):
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"                          
            data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()
        except:
            print("please provide a valid link and try again.")
            exit()
    file = open(file_path, 'wb')
    file.write(data)
    file.close()
                                         
def extract_incidents(file_path):
    with open(file_path, 'rb') as file:
        reader = PdfReader(file_path)
        page_list = list()
        for p in range(len(reader.pages)):
            text = reader.pages[p].extract_text()
            page_list.append(text)
    page_list[0] = re.sub(r"(Date \/ Time Incident Number Location Nature Incident ORI|Daily Incident Summary \(Public\))", "", page_list[0])
    substring_pg_1 = page_list[0][1:len(page_list[0]) - 1]
    page_list[0] = substring_pg_1
    page_list.pop(-1)
    lines = page_to_line(page_list)
    incidents = list()
    for line in lines:
        incidents.append(line_incident_parser(line))
    
    return incidents

def page_to_line(page_list):
    lines = list()
    for i in range(len(page_list)):
        lines_per_page = page_list[i].split('\n')
        for j in range(len(lines_per_page)):
            if not re.search(r'^\d+\/\d+\/\d+ \d+:\d+ \d{4}-\d{8}', lines_per_page[j]):
                try:
                    index = lines.index(lines_per_page[j - 1])
                    lines[index] = f'{lines_per_page[j - 1]}{lines_per_page[j]}'
                except:
                    continue    
            else:
                lines.append(lines_per_page[j])
    return lines

def line_incident_parser(line):
    line = re.sub(r'NORMAN POLICE DEPARTMENT$', '', line)
    time = re.search(r'^\d+\/\d+\/\d+ \d+:\d+', line).group(0)
    inumber = re.search(r'\d{4}-\d{8}', line).group(0)
    ori = line.split()[-1]
    line = re.sub(r'^\d+\/\d+\/\d+ \d+:\d+ \d{4}-\d{8} ', '', line)
    line = line[:line.rindex(' ')]
    nature_raw = re.findall(r'[A-Z][a-z]+', line)
    nature = ' '.join(nature_raw)
    location = line.replace(f' {nature}', '')
    
    return Incident(time, inumber, location, nature, ori)

        

        
  


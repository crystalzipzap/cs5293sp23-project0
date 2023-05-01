# CS5293sp23 – Project0

Name: Chenyi "Crystal" Zhang

# Project Description

This application populates a SQLite database based on a provided [Daily Incident Summary](https://www.normanok.gov/sites/default/files/documents/2023-04/2023-03-31_daily_incident_summary.pdf) passed via `--incident` argument tag. The argument is an valid link to the daily incident summary report in the `.pdf` format. The application downloads the file and save it in a subdirectory. Then, it parses through the content with the help of `pypdf` and `re`, converting blocks of string per page to lines of useful information, and further separates them based on categories and then use those to initalize a list of Incident objects. The aplication creates a `SQLite` database and insert the list of incidents into the database. At last, it outputs a total number of incidents grouped by nature from the database.

# How to install/run

Clone the repo and move into the directory. Then run the command below:

```shell
pipenv run python project0/main.py --incidents <link of the Daily Incident Summary>
```

Here is the command using the [March 1st Daily Incident Summary](https://www.normanok.gov/sites/default/files/documents/2023-04/2023-03-31_daily_incident_summary.pdf). Note that this link is no longer active, but since I have the file saved in the repo, this command below should still work:

```shell
pipenv run python project0/main.py --incidents https://www.normanok.gov/sites/default/files/documents/2023-04/2023-03-31_daily_incident_summary.pdf
```

Here is the command using the [April 1st Daily Incident Summary](https://www.normanok.gov/sites/default/files/documents/2023-04/2023-04-01_daily_incident_summary.pdf): 

```shell
pipenv run python project0/main.py --incidents https://www.normanok.gov/sites/default/files/documents/2023-04/2023-04-01_daily_incident_summary.pdf
```

gif to follow:

## Functions

### incident.py

| Field Type | Field    | Description                                                       |
| ---------- | -------- | ----------------------------------------------------------------- |
| String     | time     | The date and time of the incident in a format of MM/DD/YYYY 00:00 |
| String     | number   | Incident Number                                                   |
| String     | location | Address of the incident                                           |
| String     | nature   | The nature of the incident, aka reason for the visit              |
| String     | ori      | Indicent ORI                                                      |

| Constructor/ Output                                 | Description                                                                                                                                                                                                                                                                                                                                                  |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------- | --------------- | ------------- | ------------ | --- |
| **init**(self, time, number, location, nature, ori) | Create an object of Incident based on the provided time, incident, location, nature, and Incident ORI. The constructor handles two edge cases: When the location includes "HWY", and nature is "Traffic Stop", the nature would be updated to "HWY Traffic Stop" to reflect its original state. If nature is left blank, a word 'blank' would be autofilled. |
| **str**(self)                                       | define the output format for the object to be "f'{self.time}                                                                                                                                                                                                                                                                                                 | {self.number} | {self.location} | {self.nature} | {self.ori}'" |     |

### file_extraction.py

| Return Type | Function                     | Description                                                                                                                                                                                                                                                                                                                                                                                                         |
| ----------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| String      | file_path_generator(url)     | Take a hyperlink of the summary and use regular expression to extract file name then append directory in the foramt of "docs/yyyy-mm-dd_daily_incident_summary.pdf"                                                                                                                                                                                                                                                 |
| None        | fetch_incidents(url)         | Download the daily incident summary pdf file and save it in the "docs" subdirectory.                                                                                                                                                                                                                                                                                                                                |
| Incident[ ] | extract_incidents(file_path) | Open the pdf file saved in the "docs" directory and convert the data in the file to a list of Incident objects. Use PdfReader to extract the strings per page, append them into a list. Then, using the page_to_line() function to convert the string per page to a list of lines per page. Then use the line_incident_parser() to extract the fields of Incident object from each line, and initialize the object. |
| String [ ]  | page_to_line(page_list)      | A helper function. Take the list that contains all the texts per page , clean the headers and other unnecessary texts, then use split() and regular expression to convert them into a list of lines. Each line includes time, number, location, nature, and Incident ORI.                                                                                                                                           |
| Incident    | line_incident_parser(line)   | A helper function. Use split(), join(), and regular expression to extract texts for each Incident fields to initialize a single Incident object.                                                                                                                                                                                                                                                                    |

### database.py

| Return Type | Function                   | Description                                                                                                                        |
| ----------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | --- |
| Connection  | createdb()                 | Create a SQLite database named 'normanpd.db' and execute the SQL Command to create a table based on the fields of Incident object. |
| None        | populatedb(incidents_list) | Take a list of Incident objects and insert the information they contain into the database                                          |
| None        | status()                   | Output all the natures and the count of incidents per nature, separate them by '                                                   | '   |

## Tests

### pytest

I created three test files to test the given functions. Here is the output. I ran the test using the command below: |

```shell
pipenv run python -m pytest
```

All seven tests are passed. The

```shell
============================================================================================================== test session starts ==============================================================================================================
platform linux -- Python 3.10.6, pytest-7.3.1, pluggy-1.0.0
rootdir: /home/crystal_z_0616/cs5293sp23-project0
collected 7 items

project0/test_data_base.py ...                                                                                                                                                                                                            [ 42%]
project0/test_file_extraction.py ...                                                                                                                                                                                                      [ 85%]
project0/test_incident.py .                                                                                                                                                                                                               [100%]

=============================================================================================================== 7 passed in 0.75s ===============================================================================================================
```

### output test

I tested on six pdf files listed below:

**March - has been removed but these are saved in the repo**

- [March 1st](docs/2023-03-01_daily_incident_summary.pdf)
- [March 15th](docs/2023-03-15_daily_incident_summary.pdf)
- [March 31st](docs/2023-03-31_daily_incident_summary.pdf)

**April - active links**

- [April 1st](https://www.normanok.gov/sites/default/files/documents/2023-04/2023-04-01_daily_incident_summary.pdf)
- [April 15th](https://www.normanok.gov/sites/default/files/documents/2023-04/2023-04-15_daily_incident_summary.pdf)
- [April 25th](https://www.normanok.gov/sites/default/files/documents/2023-04/2023-04-25_daily_incident_summary.pdf)

## Database Development

I applied three SQL commands to populate database and query the information for the output.

1. Create the table named incidents and include five fields based on the format of the pdf file.

```sql
CREATE TABLE IF NOT EXISTS incidents
                (incident_time TEXT,
                incident_number TEXT,
                incident_location TEXT,
                nature TEXT,
                incident_ori TEXT);
```

2. Insert information extracted from the file to the database.

```sql
INSERT INTO incidents VALUES (
    incident.time,
    incident.number,
    incident.location,
    incident.nature,
    incident.ori
)
```

3. Output count of incidents per nature.

```sql
SELECT nature, COUNT(*)
FROM incidents
WHERE nature != '' GROUP BY nature
```

## Bugs and Assumptions

### Assumptions

- A correct daily incident summary link is provided at the command line when running the program.
  - The program should exit if a link is not provided. But it cannot handle an incorrect link.
- Pytest runs before using the application. To pass the database test, I had to delete the database once the test is complete. If Pytest runs after using the application, the data saved in the database will be lost.

### Known Bugs

- When testing with the 03-01-2023 Daily Incident Summary file, I encountered 2 entries where the nature fields were "blank". It seems like my parser wasn't able to handle some newlines perfectly.
- I encountered issue when nature includes uppercase letters. The reason is when separating line to the fields for the Incident Object, I set the regular expression to first identify the well-formatted fields like time and ORI, then extract address by finding all cap strings and extract Nature from the rest of the mixed case strings. I came up with this strategy after reviewing the format of the document. The one I am aware is the nature "HWY Traffic Stop". I attempted to handle it by hard coding the check in the Incident class. It works to a degree but is not perfect.

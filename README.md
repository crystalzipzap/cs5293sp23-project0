# CS5293sp23 – Project0

Name: Chenyi "Crystal" Zhang

# Project Description

This application populates a SQLite database based on a provided [Daily Incident Summary](https://www.normanok.gov/sites/default/files/documents/2023-04/2023-03-31_daily_incident_summary.pdf) passed via `--incident` argument tag. The argument is an valid link to the daily incident summary report in the `.pdf` format. The application downloads the file and save it in a subdirectory. Then, it parses through the content with the help of `pypdf` and `re`, converting blocks of string per page to lines of useful information, and further separates them based on categories and then use those to initalize a list of Incident objects. The aplication creates a `SQLite` database and insert the list of incidents into the database. At last, it outputs a total number of incidents grouped by nature from the database.

# How to install

## How to run

## Functions

ou should describe all functions and your approach to developing the database

## Test

## Database Development

## Bugs and Assumptions

We know your code will not be perfect, be sure to include any assumptions you make for your solution.

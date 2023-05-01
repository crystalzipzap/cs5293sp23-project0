# -*- coding: utf-8 -*-
# Example main.py
import argparse
import sqlite3
from file_extraction import fetch_incidents, file_path_generator, extract_incidents
from database import createdb, populatedb, status


def main(url):
    # Download and extract data
    file_path = file_path_generator(url)
    fetch_incidents(url)
    incidents = extract_incidents(file_path)
	
    # Create new database
    connect = sqlite3.connect('normanpd.db')
    createdb()
	
    # Insert data
    populatedb(incidents)
	
    # Print incident counts
    status()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="Incident summary url.")
    
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
    else: 
        print("Error: --incidents argument is required.")
        print("Please rerun the application with the correct argument.")
        exit()
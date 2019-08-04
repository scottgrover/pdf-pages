#!/bin/python3

import pdfkit
import sys
import sqlite3
import os
import pandas

sqlite_file = 'pdf-pages.sqlite' 

def print_usage():
    print("pdf-pages.py - A CLI tool to store web pages in pdf form.")
    print("Usage:")
    print("-----------------------------------------------------------------------------------")
    print("Initialize database:         python3 pdf-pages init")
    print("Download stored web pages:   python3 pdf-pages download")
    print("Add to database:             python3 pdf-pages add <url> <file path>")
    print("Delete from database:        python3 pdf-pages delete <full path to file name>")
    print("Add csv to database:         python3 pdf-pages csv <file_name>")
    print("-----------------------------------------------------------------------------------")

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def create_row(conn, row):
    """
    Create a new row into the documents table
    :param conn:
    :param row:
    """
    sql = ''' INSERT INTO documents(url,filepath)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, row)
    print("Added new row.")
    return   

def yes_or_no(question):
    """ Get a yes or no input to a question
    :param question: yes or no question
    :return: boolean for response
    """
    reply = str(input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("Unexpected response, please enter ")

def init():
    if os.path.exists(sqlite_file):
        confirmation = yes_or_no("A sqlite db exists, would you like to overwrite the existing db?")
        if confirmation == True:
            os.remove(sqlite_file)
        else: 
            print("Exiting...")
            return
    else:
        confirmation = True

    if confirmation == True:
        print("Initializing new sqlite database...")
        table_name = 'documents'  # name of the table to be created
        url_field = 'url' # name of the field
        filepath_field = 'filepath' # name of the field
        field_type = 'TEXT'  # field data type

        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()

        c.execute('CREATE TABLE {tn} ({uf} {ut}, {fpf} {fpt})'\
            .format(tn=table_name, uf=url_field, ut=field_type,fpf=filepath_field, fpt=field_type))

        conn.commit()
        conn.close()

def add():
    if os.path.exists(sqlite_file):
        if len(sys.argv) != 4:
            print("Arguments are needed.")
            print_usage()
            return
        conn = create_connection(sqlite_file)
        with conn:
            newRow = (sys.argv[2], sys.argv[3])
            create_row(conn, newRow)
        conn.close()
    else: 
        print("pdf-pages sqlite database doesn't exist.")
        create = yes_or_no("Would you like to create one?")
        if create == True:
            init()
            conn = create_connection(sqlite_file)
            with conn:
                newRow = (sys.argv[2], sys.argv[3])
                create_row(conn, newRow)
            conn.close()

def delete():
    if os.path.exists(sqlite_file):
        if len(sys.argv) != 3:
            print("Arguments are needed.")
            print_usage()
            return
        conn = create_connection(sqlite_file)
        with conn:
            fileName = sys.argv[2]
            sql = 'DELETE FROM documents WHERE filepath=?'
            cur = conn.cursor()
            cur.execute(sql, (fileName,))
            print("Deleted row.")
        conn.close()
        return
    else: 
        print("pdf-pages sqlite database doesn't exist.")
        create = yes_or_no("Would you like to create one?")
        if create == True:
            init()
        else:
            return

def query_db(query):
    conn = create_connection(sqlite_file)
    with conn:
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
    conn.close()
    return rows

def download():
    rows = query_db("SELECT * FROM documents")

    for row in rows:
        url = row[0]
        filepath = row[1]

        if os.path.exists(filepath):
            print("File ", filepath, "exists. Skipping...")
        else:
            print("Downloading ", url, "saving to:", filepath)
            pdfkit.from_url(url, filepath)

def show():
    rows = query_db("SELECT * FROM documents")
    for row in rows:
        print("| Source URL:", row[0], "| File Name:", row[1], " |")

def csv(): 
    print("Take csv and add each entry to db")
    conn = create_connection(sqlite_file)
    with conn:
        df = pandas.read_csv(sys.argv[2])
        df.to_sql("documents", conn, if_exists='replace', index=False)
    conn.close()

def main():
    if sys.argv[1] == "init":
        init()
    elif sys.argv[1] == "add":
        add()
    elif sys.argv[1] == "delete":
        delete()
    elif sys.argv[1] == "download":
        download()
    elif sys.argv[1] == "show":
        show()
    elif sys.argv[1] == "csv":
        csv()
    elif sys.argv[1] == "help":
        print_usage()
    else: 
        print("Unknown command:", sys.argv[1])
        print_usage()

main()
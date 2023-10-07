import os
import shutil
import numpy as np
import mysql.connector
from envs import *
import ipdb
import time
import datetime

def create_tables(mysql_keys, tables):
    """
    Create the desired tables
    """
    connector = mysql.connector.connect(**mysql_keys)
    cursor = connector.cursor()
    for table in tables:
        try:
            cursor.execute(table)
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR: 
                print('Table already exists')
            else:
                print(err.msg)
                print("Table: %s"%table[13:30])
    connector.commit()
    cursor.close()
    connector.close()
    return 1



def read_file(filename, date=True):
    """
    Read the info from the file at the frontend computer
    """
    content = np.loadtxt(filename, dtype=str, delimiter=' ',skiprows=10, usecols=(0,1))
    stamp = content[:,0].astype(float)
    data = content[:,1]
    mask = data=='----'
    data[mask] = None#np.nan
    #ipdb.set_trace()
    data = data.astype(float)
    if(date):
        stamp = [datetime.datetime.fromtimestamp(x) for x in stamp]
    return stamp, data



def populate_sensors_database(mysql_keys, folder_list, Variables):
    """
    Reads the files from the computer and insert them into the database

    mysql_keys: The keys to enter to the database
    folder_list: a list with the folders that you want to upload (its is the one with the name)
    Variables: variables defined in env.py
    """
    connector = mysql.connector.connect(**mysql_keys)
    cursor = connector.cursor()
    ##
    for folder in folder_list:
        print("Folder: %s"%(folder))
        for variable in Variables:
            print("\tVariable: %s"%variable['names'][0])
            for file, insert in zip(variable['folders'], variable['insert']):
                filename = os.path.join(folder, file)
                stamp, data = read_file(filename)
                for timestamp,dat in zip(stamp, data):
                    #ipdb.set_trace()
                    try:
                        cursor.execute(insert%(str(timestamp), dat))
                    except mysql.connector.Error as err:
                        #ipdb.set_trace()
                        if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
                            print('Data already exists {}, {}'.format(timestamp, dat))
                            #print(err.msg)
                        else:
                            print(err.msg)
                connector.commit()
    cursor.close()
    connector.close()



def query_data(mysql_keys, queries, dates, conditions=''):
    """
    This function returns the timestamp and the value of the query

    mysql_keys: keys for the connection
    queries: list with the query formatting  (this come from the Variables dictionary at env.py)
    dates: list with datatime objects, determine the starting and ending date
    conditions: additional conditions (eg: AND temperature<100)
    """
    connector = mysql.connector.connect(**mysql_keys)
    cursor = connector.cursor()
    out = []
    for query in queries:
        msj = query%(dates[0], dates[1])
        msj += conditions
        cursor.execute(msj)
        result = cursor.fetchall()
        out.append(result)
    return out
        
        

if __name__ == '__main__':
    folders = os.listdir(sensors_local_folder)
    folders.sort()
    #im going to initialize a database 
    connector = mysql.connector.connect(
            host = mysql_keys['host'],
            port = mysql_keys['port'],
            user = mysql_keys['user'],
            password = mysql_keys['password']
            )
    cursor = connector.cursor()
    cursor.execute('drop database '+mysql_keys['database'])
    cursor.execute('create database '+mysql_keys['database'])
    cursor.close()
    connector.close()
    time.sleep(1)
    #first we are going to create the tables
    tables = []
    for variable in Variables:
        tables += variable['table_init']
    print("Creating the tables")
    create_tables(mysql_keys, tables)
    folders = [os.path.join(sensors_local_folder, x) for x in folders]
    print("Populating the tables")
    populate_sensors_database(mysql_keys, folders, Variables)
    #query example
    dates = (datetime.datetime(2023,9,1), datetime.datetime(2023,9,2))
    queries = (Variables[0]['query'][0], Variables[0]['query'][1])
    additional_conditions = "AND temperature<0.35"
    
    print("reading {} and {} information".format(Variables[0]['nickname'][0], Variable[0]['nickname'][1]))
    data = query_data(mysql_keys, queries,dates, additional_conditions)


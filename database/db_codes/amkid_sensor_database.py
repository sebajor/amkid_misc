import os
import time
import datetime
import shutil
import ipdb
import mysql.connector
import numpy as np
from envs import *


def read_file_type1(filename, date=True):
    """
    Read the info from the file at the frontend computer
    This function works with cryocon, lakeshore_temp and sumitomo
    TODO: extend to the other sensors
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



class amkid_sensor_database():

    def __init__(self, 
                 mysql_keys=None, 
                 sensor_folder='../data',
                 ):
        """
        Here I define all the variables
        """
        if(mysql_keys is None):
            self.mysql_keys = {
                'host':'localhost',
                'port':33060,
                'user':'root',
                'password':'amkid',
                'database':'test'
                }
        else:
            self.mysql_keys = mysql_keys
        
        self.sensor_folder = sensor_folder
        ##definitions the fields
        self.Variable = {}
        self.init_cryocon_fields()
        self.init_lakeshore_temp_field()
        self.init_Lakeshore_relay_fields()
        self.init_Sumitomo_fields()
        self.init_Vacuum_fields()


    
    ###
    ### Iniitalize of the sql messages for each sensor
    ###
    def init_cryocon_fields(self, folders=None, names=None,nickname=None,
                            table_init=None,insert=None,query=None):
        """
        folders: Name of the files in the Cyocon folders
        names:  
        nickname:identifier at the file, this is also the name of the table
        table_init: string to create the table
        insert: string to populate the table
        query: string to make a query 
        """
        Cryocon = {}
        Cryocon['folders'] = ['CryoCon/Temp'+str(x) for x in range(1,6)]
        Cryocon['names'] = ['Cryocon_temp'+str(x) for x in range(1,6)]
        Cryocon['nickname'] = ['U_HEAD', 'I_HEAD', 'He4_HEAD', 'LFA_array', 'HFA_array']
        Cryocon['table_init'] = ["CREATE TABLE `{}` (   `tstamp` datetime,   `temperature` double,    PRIMARY KEY (`tstamp`)) ".format(Cryocon['nickname'][x]) for x in range(0,5)]
        Cryocon['insert'] = ["INSERT INTO {} (tstamp, temperature) VALUES ('%s',%s)".format(Cryocon['nickname'][x]) for x in range(0,5)]
        Cryocon['query'] = ["SELECT tstamp,temperature  FROM  {}.{}     WHERE tstamp BETWEEN '%s' AND '%s'".format(self.mysql_keys['database'], Cryocon['nickname'][x]) for x in range(0,5)]
        Cryocon['last_timestamp'] = [None]*5
        self.Variable['Cryocon'] = Cryocon


    def init_lakeshore_temp_field(self, folders=None, names=None,nickname=None,
                                  table_init=None,insert=None,query=None):
        Lakeshore_temp = {}
        Lakeshore_temp['folders']= ['Lakeshore/Temp'+str(x) for x in range(1,17)]

        Lakeshore_temp['names'] = ['Lakeshore_temp'+str(x) for x in range(1,17)]
        Lakeshore_temp['nickname'] = [
                'HE10_BUFFER_PUMP', 'HE10_ULTRA_SWITCH', 'HE10_INTER_SWITCH',
                'HE10_BUFFER_SWITCH', 'HE10_FILM_BURNER', 'HE10_ULTRA_PUMP',
                'HE10_INTER_PUMP', 'HOT_LOAD_temp', '77K_SHIELD_COOLER',
                '77K_HE10_COOLER', '77K_SHIELD', '77K_WINDOW',
                '4K_AMPLIFIER_BLOCK', '4K_WINDOW', '4K_HE10_BATH',
                '4K_HE10_COOLER']
        Lakeshore_temp['table_init'] = ["CREATE TABLE `{}` (   `tstamp` datetime,   `temperature` double,     PRIMARY KEY (`tstamp`)) ".format(Lakeshore_temp['nickname'][x]) for x in range(0,16)]
        Lakeshore_temp['insert'] = ["INSERT INTO {} (tstamp, temperature) VALUES ('%s',%s)".format(Lakeshore_temp['nickname'][x]) for x in range(0,16)]
        Lakeshore_temp['query'] = ["SELECT tstamp,temperature  FROM  {}.{}     WHERE tstamp BETWEEN '%s' AND '%s'".format(self.mysql_keys['database'], Lakeshore_temp['nickname'][x]) for x in range(0,16)]
        Lakeshore_temp['last_timestamp'] = [None]*16

        self.Variable['Lakeshore_temp'] = Lakeshore_temp


    def init_Lakeshore_relay_fields(self, folders=None, names=None,nickname=None,
                            table_init=None,insert=None,query=None):
        Lakeshore_relay ={}
        Lakeshore_relay['folders']= ['Lakeshore/Relay'+str(x) for x in range(1,9)]
        Lakeshore_relay['names'] = ['Lakeshore_relay'+str(x) for x in range(1,9)]
        Lakeshore_relay['nickname'] = Lakeshore_relay['names']
        Lakeshore_relay['table_init'] = ["CREATE TABLE `Lakeshore_relay{}` (   `tstamp` datetime,   `relay` double,     PRIMARY KEY (`tstamp`)) ".format(x) for x in range(1,9)]
        Lakeshore_relay['insert'] = ["INSERT INTO Lakeshore_relay{} (tstamp, temperature) VALUES ('%s',%s)".format(x) for x in range(1,9)]
        Lakeshore_relay['last_timestamp'] = [None]*8
        self.Variable['Lakeshore_relay'] = Lakeshore_relay


    def init_Sumitomo_fields(self, folders=None, names=None,nickname=None,
                      table_init=None,insert=None,query=None):
        Sumitomo = {}
        Sumitomo['folders']= ['Sumitomo/RetPressure1', 'Sumitomo/RetPressure2']
        Sumitomo['names'] = ['Sumitomo_pressure'+str(x) for x in range(1,3)]
        Sumitomo['table_init'] = ["CREATE TABLE `Sumitomo_pressure{}` (   `tstamp` datetime,   `pressure` float,     PRIMARY KEY (`tstamp`)) ".format(x) for x in range(1,3)]
        Sumitomo['insert'] = ["INSERT INTO Sumitomo_pressure{} (tstamp, pressure) VALUES ('%s',%s)".format(x) for x in range(1,3)]
        Sumitomo['query'] = ["SELECT tstamp,pressure  FROM  Sumitomo_pressure{} WHERE tstamp BETWEEN '%s' AND '%s'".format(self.mysql_keys['database'], x) for x in range(1,3)]
        Sumitomo['last_timestamp'] = [None]*2
        self.Variable['Sumitomo'] = Sumitomo

    
    def init_Vacuum_fields(self, folders=None, names=None,nickname=None,
                      table_init=None,insert=None,query=None):
        Vacuum = {}
        Vacuum['folders'] = ['Vacuum/Vacuum1','Vacuum/Vacuum2']
        Vacuum['names'] = ['Vacuum'+str(x) for x in range(1,3)]
        Vacuum['table_init'] = ["CREATE TABLE `Vacuum{}` (   `tstamp` datetime,   `pressure` double,     PRIMARY KEY (`tstamp`)) ".format(x) for x in range(1,3)]
        Vacuum['insert'] = ["INSERT INTO Vacuum{} (tstamp, pressure) VALUES ('%s',%s)".format(x) for x in range(1,3)]
        Vacuum['query'] = ["SELECT tstamp,pressure  FROM  Vacuum{} WHERE tstamp BETWEEN '%s' AND '%s'".format(self.mysql_keys['database'], x) for x in range(1,3)]
        Vacuum['last_timestamp'] = [None]*2
        self.Variable['Vacuum'] = Vacuum

    ###
    ### Query functions
    ###
    
    def create_tables(self, tables=None):
        """
        Create the tables in the database at mysql_keys
        tables: tables creation query messages
        """
        connector = mysql.connector.connect(**self.mysql_keys)
        cursor = connector.cursor()
        if(tables is None):
            #generate all the tables
            tables = []
            for key, item in self.Variable.items():
                tables += item['table_init']
        else:
            tables = tables
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

    def populate_sensors_database(self, folder_list):
        """
        Reads the files from the computer and insert them into the database..

        folder_list: a list with the folders that you want to upload (its is the one with the name)
        last_timestamp: contains the last datetime object uploaded
                       
        """
        connector = mysql.connector.connect(**self.mysql_keys)
        cursor = connector.cursor()
        folder_list.sort()
        ##
        for folder in folder_list:
            ipdb.set_trace()
            print("Folder: %s"%(folder))
            for keys, variable in self.Variable.items():
                print("\tVariable: %s"%variable['names'][0])
                for file, insert, last_stamp in zip(variable['folders'], 
                                                    variable['insert'],
                                                    variable['last_timestamp']):
                    filename = os.path.join(folder, file)
                    stamp, data = read_file_type1(filename)
                    if(last_stamp is not None):
                        mask = stamp>last_stamp
                        stamp = stamp[mask]
                        data = data[mask]
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
                    if(len(stamp)>1):
                        ###only update if it wrote data into the db
                        variable['last_timestamp'] = stamp[-1]
                    connector.commit()
        cursor.close()
        connector.close()

     
    def query_data(self, queries, dates, conditions=''):
        """
        This function returns the timestamp and the value of the query

        queries: list with the query formatting  (this come from the Variables dictionary at env.py)
        dates: list with datatime objects, determine the starting and ending date
        conditions: additional conditions (eg: AND temperature<100)
        """
        connector = mysql.connector.connect(**self.mysql_keys)
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
    sensor_local_folder = '../data'
    folders = os.listdir(sensors_local_folder)
    folders.sort()
    ##initialize the database
    mysql_keys = {
        'host':'localhost',
        'port':33060,
        'user':'root',
        'password':'amkid',
        'database':'test'
        }
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
    ###
    amkid_db = amkid_sensor_database() 
    print('Creating tables')
    amkid_db.create_tables()
    
    folders = [os.path.join(sensors_local_folder, x) for x in folders]
    print("Populating the tables")
    amkid_db.populate_sensors_database(folders)

    print('Reading from the database')
    #amkid_db
     
    










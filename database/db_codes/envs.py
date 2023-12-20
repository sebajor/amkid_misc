###
###database parameters
###
mysql_keys = {
        'host':'localhost',
        'port':33060,
        'user':'root',
        'password':'amkid',
        'database':'test'
        }
###
###sensors 
###

sensors_remote_folder = '/home/amkid/Database/AMKID'
sensors_local_folder = '../AMKID'

##Data to save in the 

Cryocon = {}
Lakeshore_temp = {}
Lakeshore_relay ={}
Sumitomo = {}
Vacuum = {}


##we need double presicion in the timestamp otherwise all the data is approximated and have the same key
##
Cryocon['folders'] = ['CryoCon/Temp'+str(x) for x in range(1,6)]
Cryocon['names'] = ['Cryocon_temp'+str(x) for x in range(1,6)]
Cryocon['nickname'] = ['U_HEAD', 'I_HEAD', 'He4_HEAD', 'LFA_array', 'HFA_array'] 
Cryocon['table_init'] = ["CREATE TABLE `{}` (   `tstamp` datetime,   `temperature` double,    PRIMARY KEY (`tstamp`)) ".format(Cryocon['nickname'][x]) for x in range(0,5)]
Cryocon['insert'] = ["INSERT INTO {} (tstamp, temperature) VALUES ('%s',%s)".format(Cryocon['nickname'][x]) for x in range(0,5)]
Cryocon['query'] = ["SELECT tstamp,temperature  FROM  {}.{}     WHERE tstamp BETWEEN '%s' AND '%s'".format(mysql_keys['database'], Cryocon['nickname'][x]) for x in range(0,5)]

##
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
Lakeshore_temp['query'] = ["SELECT tstamp,temperature  FROM  {}.{}     WHERE tstamp BETWEEN '%s' AND '%s'".format(mysql_keys['database'], Lakeshore_temp['nickname'][x]) for x in range(0,16)]



Lakeshore_relay['folders']= ['Lakeshore/Relay'+str(x) for x in range(1,9)]
Lakeshore_relay['names'] = ['Lakeshore_relay'+str(x) for x in range(1,9)]
Lakeshore_relay['table_init'] = ["CREATE TABLE `Lakeshore_relay{}` (   `tstamp` datetime,   `relay` double,     PRIMARY KEY (`tstamp`)) ".format(x) for x in range(1,9)]
Lakeshore_relay['insert'] = ["INSERT INTO Lakeshore_relay{} (tstamp, temperature) VALUES ('%s',%s)".format(x) for x in range(1,9)]

Sumitomo['folders']= ['Sumitomo/RetPressure1', 'Sumitomo/RetPressure2']
Sumitomo['names'] = ['Sumitomo_pressure'+str(x) for x in range(1,3)]
Sumitomo['table_init'] = ["CREATE TABLE `Sumitomo_pressure{}` (   `tstamp` datetime,   `pressure` float,     PRIMARY KEY (`tstamp`)) ".format(x) for x in range(1,3)]
Sumitomo['insert'] = ["INSERT INTO Sumitomo_pressure{} (tstamp, pressure) VALUES ('%s',%s)".format(x) for x in range(1,3)]
Sumitomo['query'] = ["SELECT tstamp,pressure  FROM  Sumitomo_pressure{} WHERE tstamp BETWEEN '%s' AND '%s'".format(mysql_keys['database'], x) for x in range(1,3)]

Vacuum['folders'] = ['Vacuum/Vacuum1','Vacuum/Vacuum2']
Vacuum['names'] = ['Vacuum'+str(x) for x in range(1,3)]
Vacuum['table_init'] = ["CREATE TABLE `Vacuum{}` (   `tstamp` datetime,   `pressure` double,     PRIMARY KEY (`tstamp`)) ".format(x) for x in range(1,3)]
Vacuum['insert'] = ["INSERT INTO Vacuum{} (tstamp, pressure) VALUES ('%s',%s)".format(x) for x in range(1,3)]
Vacuum['query'] = ["SELECT tstamp,pressure  FROM  Vacuum{} WHERE tstamp BETWEEN '%s' AND '%s'".format(mysql_keys['database'], x) for x in range(1,3)]



Variables = [Cryocon, Lakeshore_temp, Sumitomo] #, Vacuum, Lakeshore_relay]


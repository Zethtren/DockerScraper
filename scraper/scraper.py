import asyncio
from datetime import datetime
import pyodbc
import os
import time
from copra.websocket import Channel, Client

import pyodbc

# TODO: Currently logs to console. Add option for saving external logs.

# File variables imported from default ENV variables supplied by dockerfile or overwritten by docker-compose.yml

if os.environ.get("LOG_INSERTS"):
    
    log_inserts = os.environ.get("LOG_INSERTS") 
    
    if str.lower(log_inserts) == 'false': 
        log_inserts = False
    else:
        log_inserts = True
    
    print(f"LOG_INSERTS set to: {log_inserts}")
else:
    log_inserts = True
    print(f"LOG_INSERTS defaulted to: True")

if os.environ.get("SERVER_NAME"):
    server = os.environ.get("SERVER_NAME") 
    print(f"Collected SERVER_NAME: {server}")
else:
    server = 'sql-server'
    print(f"SERVER_NAME defaulted to: {server}")

if os.environ.get("DB_NAME"):
    database = os.environ.get("DB_NAME") 
    print(f"Collected DB_NAME: {database}")
else:
    database = 'ticks'
    print(f"DB_NAME defaulted to: {database}")

if os.environ.get("TABLE_NAME"):
    table_name = os.environ.get("TABLE_NAME")
    print(f"Collected TABLE_NAME_NAME: {table_name}")
else:
    table_name = 'BTC-USD'
    print(f"Default TABLE_NAME used: {table_name}")

if os.environ.get("SA_PASSWORD"):
    password = os.environ.get("SA_PASSWORD")
    print(f"Collected SA_PASSWORD: *********")
else:    
    password = 'asdffdsaasdffdsa1234!'
    print("Default Password asdffdsaasdffdsa1234! used")
    print("This is fine for debugging but custom passwords should be used in development")

if os.environ.get("TABLE_NAME"):
    product_id = os.environ.get("TABLE_NAME")
else:
    product_id = 'BTC-USD'
    print("Invalid Market selected. Default \"BTC-USD\" used")
    print("General Error tests only for existence of Coin Pair. Not validity of said Coin Pair")

username = 'sa' # Default user made by SQL Server on spinup
print("UserName: sa")




not_connected = True
while not_connected:
    try:
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        not_connected = False
        print("Connection Established")
    except Exception:
        time.sleep(5)
        print("Connection Not established yet. Trying again in 5 seconds.")



# Check for table existence and create table if necessary
# Data Types are intentionally large to account for market diversity. Feel free to adjust these values.

cursor.execute(f"IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='[{table_name}]' AND xtype='U') CREATE TABLE [{table_name}] (price Decimal(18,10), bid Decimal(18,10), ask Decimal(18,10), side VARCHAR(5), time DATETIMEOFFSET(7), size Decimal(18,10), trade_id BIGINT)")




class Ticker(Client):

    def on_message(self, message):
        """
        Overwrite of asyncio on_message implementation in copra library see: https://github.com/tpodlaski/copra
        
        This funtion executes whenever a message is received from the websocket:
        
        TODO: 
                - Include duplicate check logic to allow multiple node spinnups
                - Improve Error specificity
        """
        try:
            if message['type'] == 'ticker' and 'time' in message:
                
                # Cast values and insert into tuple for reduced RAM overhead
                insert_tuple = (float(message['price']), \
                                float(message['best_bid']), \
                                float(message['best_ask']), \
                                message['side'], \
                                message['time'], \
                                float(message['last_size']), \
                                int(message['trade_id'])) 
               
                # Insert Values into SQL Server
                cursor.execute(f"""INSERT INTO [dbo].[{table_name}] (price, bid, ask, side, time, size, trade_id)
                VALUES {insert_tuple}""") 
                cnxn.commit()
                if log_inserts:
                    print(insert_tuple)
        except Exception:
            print(f"""SQL Insert failed for 
                                    ({float(message['price'])}, 
                                     {float(message['best_bid'])}, 
                                     {float(message['best_ask'])}, 
                                     {message['side']}, 
                                     {message['time']}, 
                                     {float(message['last_size'])}, 
                                     {int(message['trade_id'])}) """)
            print("General Error message working on refinement")                         
            # An outer catch needs to replace this for debugging purposes



loop = asyncio.get_event_loop()

channel = Channel('ticker', product_id)

ticker = Ticker(loop, channel)


try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(ticker.close())
    loop.close()
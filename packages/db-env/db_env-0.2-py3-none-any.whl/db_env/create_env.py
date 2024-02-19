# import for testing
import sqlite3


# Function - creating DB and connecting to it
def create_connect_db(db_name:str):
    '''
    - create and connect to unique database within your folder
    - use string for db_name and ending .db (e.g. "zoo.db")
    '''
    global cursor
    global connection
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        print("DONE - connected and created database")
    except:
        print("ERROR - can not create/connect to DB. Check connection or if database-name already exists")


# Function - creating table
def create_table_sql(sql_string:str):
    '''
    - create table function which uses string as an input
    - e.g. "DROP TABLE IF EXISTS CUSTOMERS;CREATE TABLE CUSTOMERS(NAME VARCHAR(30),AGE INTEGER, ORDER_ID INTEGER);"
    - Info: uses executescript instead of execute so that more than one sql statement in one execute is possible'''
    try:
        cursor.executescript(sql_string)
        connection.commit
        print("DONE - created table")
    except:
        print("ERROR - can't create table. Please check inserted string and if databbase exists")






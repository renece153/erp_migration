from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import dm_get_key_vault_creds as kv
import pyodbc
import pandas as pd
import numpy as np


def create_connection_string():
    _driver = 'ODBC Driver 17 for SQL Server'
    _server = 'RTORRECAMPO'
    _database = 'dm_test_d2d_replication'
    _username = kv.get_key_vault_secrets('localUsername')
    _password = kv.get_key_vault_secrets('localPassword')
    _port = '1433'
    connection_string = f"DRIVER={{{_driver}}};SERVER={_server};DATABASE={_database};UID={_username};PWD={_password};PORT={_port};"
    print(connection_string)
    return connection_string

def output_engine():
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": create_connection_string()})
    return create_engine(connection_url)


def exract_list_of_fields():
    db_creds = create_connection_string()
    con = pyodbc.connect(db_creds, timeout=600, autocommit = True)
    cursor = con.cursor()
    try:
        sql_query = "select field_to_extract from dm_test_d2d_replication.dbo.list_of_fields"
        cursor.execute(sql_query)
        row_set = cursor.fetchall()
        get_columns = [column[0] for column in cursor.description]
        return_set = pd.DataFrame(np.array(row_set), columns=get_columns)
        return return_set.values.tolist()
    except Exception as e:
        print(str(e))

def exract_column_name():
    db_creds = create_connection_string()
    con = pyodbc.connect(db_creds, timeout=600, autocommit = True)
    cursor = con.cursor()
    try:
        sql_query = "select column_name_in_table from dm_test_d2d_replication.dbo.list_of_fields"
        cursor.execute(sql_query)
        row_set = cursor.fetchall()
        get_columns = [column[0] for column in cursor.description]
        field_list = pd.DataFrame(np.array(row_set), columns=get_columns)
        return field_list.values.tolist()
    except Exception as e:
        print(str(e))
#import sqlite3
import pyodbc
#import os 
server = 'flaskwebapp-db-server.database.windows.net'
database = 'FlaskWebAppDB'
username = 'gyodicvvja@flaskwebapp-db-server.database.windows.net'
password = 'JDVY5MHFF6B3X433$'
driver= '{ODBC Driver 18 for SQL Server}'

conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"

#conn = pyodbc.connect(conn_str)

def get_db():
    conn = pyodbc.connect(conn_str)
    return conn


def check_db_exist():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    if not cursor.fetchall():
        script = open('Website1/schema.sql').read()
        conn.executescript(script)
        conn.close()


def run_query(sql):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return results


def execute_sql(sql, *args):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql, args)
    conn.commit()
    conn.close()


def validate_invoice_form(customername, customeraddress, date, description, invoiceno, invoicetotal):
    if len(customername) < 2:
        return 'Enter customer name'
        
    if len(customeraddress) < 3:
        return 'Address can\'t be less then 3 characters'
    
    if date is None or date == '':
        return 'Please add a date.'
            
    if len(description) < 1:
        return 'Please add a description'
    
    if len(invoiceno) < 1:
        return 'Enter invoice number'     
       
    if len(invoicetotal) < 1:
        return 'Enter invoice total.'
               
    return None     


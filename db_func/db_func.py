#import sqlite3
import pyodbc
#import os 

# Setting up connection string for connecting to Azure SQL database
server = 'flaskwebapp-db-server.database.windows.net'
database = 'FlaskWebAppDB'
username = 'gyodicvvja@flaskwebapp-db-server.database.windows.net'
password = 'JDVY5MHFF6B3X433$'
driver= '{ODBC Driver 18 for SQL Server}'
conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"

# This function gets a database connection
def get_db():
    try:
        # Try to establish a database connection using the connection string
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as e:
        # If an error occurs, print an error message and return None
        print(f"An error occurred while connecting to the database: {e}")
        return None

# This function executes a SQL query and return results
def run_query(sql):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return results

# This function executes a SQL statement that inserts/updates the database
def execute_sql(sql, *args):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql, args)
    conn.commit()
    conn.close()

# This function is to validate invoice form data
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


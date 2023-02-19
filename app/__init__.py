from flask import Flask, Blueprint, render_template, request, flash, redirect
#import sqlite3
from datetime import datetime
from db_func import execute_sql, get_db, run_query, validate_invoice_form
#import os 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

@app.route('/',  methods=['GET','POST'])
def home():
    return render_template("home.html")

@app.route('/addinvoice', methods = ['GET', 'POST'])
def addinvoice(): 
         
    if request.method == 'POST':
                
        customername = request.form.get('customername')
        customeraddress = request.form.get('customeraddress')
        date = request.form.get('date')       
        description = request.form.get('desp')
        invoiceno = request.form.get('invoiceno')
        invoicetotal = request.form.get('invoicetotal')
        flash('Invoice added!', category='greenlight')
        
        # error = db_func.validate_invoice_form(customername, customeraddress, date, description, invoiceno, invoicetotal)
        # if error is not None:
        #     flash(error, category='redlight')
        # else:
        #     #date_obj = datetime.strptime(date, '%Y-%m-%d')  # Convert the string to a datetime object
        #     #date_formatted = date_obj.strftime('%d/%m/%y')  # Convert the datetime object to a formatted string         
        #     #db_func.check_db_exist()
        #     db_func.execute_sql('INSERT INTO invoice (customername, customeraddress, date, description, invoiceno, invoicetotal) VALUES (?, ?, ?, ?, ?, ?)', customername, customeraddress, date, description, invoiceno, invoicetotal)
        #     flash('Invoice added!', category='greenlight')
          
    return render_template("Form.html")


if __name__ == '__main__':
    app.secret_key = 'asdasdasd'
    app.run(debug=True)



#gunicorn --bind=0.0.0.0 --timeout 600 startup:app
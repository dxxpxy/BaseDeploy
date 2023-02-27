from flask import Flask, Blueprint, render_template, request, flash, redirect
#import sqlite3
from datetime import datetime
from db_func.db_func import get_db, validate_invoice_form, execute_sql, run_query
#import db_func
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
        
        error = validate_invoice_form(customername, customeraddress, date, description, invoiceno, invoicetotal)
        if error is not None:
            flash(error, category='redlight')
        else:
            #date_obj = datetime.strptime(date, '%Y-%m-%d')  # Convert the string to a datetime object
            #date_formatted = date_obj.strftime('%d/%m/%y')  # Convert the datetime object to a formatted string         
            #db_func.check_db_exist()
            execute_sql('INSERT INTO invoice (customername, customeraddress, date, description, invoiceno, invoicetotal) VALUES (?, ?, ?, ?, ?, ?)', customername, customeraddress, date, description, invoiceno, invoicetotal)
            flash('Invoice added!', category='greenlight')
          
    return render_template("Form.html")

@app.route('/viewinvoice')
def viewinvoice():
    
    invoices = run_query('SELECT * FROM invoice')
    return render_template("invoice.html", invoices=invoices) 

@app.route('/editinvoice/<int:invoice_id>', methods=['GET', 'POST'])
def editinvoice(invoice_id):
    # Connect to database and retrieve invoice data
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM invoice WHERE id = ?', (invoice_id,))
    invoice = cursor.fetchone()
    conn.close()

    if request.method == 'POST':
        # Retrieve new invoice total from form data
        new_customername = request.form['customername']
        new_customeraddress = request.form['customeraddress']
        new_date = request.form['date']
        new_description = request.form['desp']
        new_invoiceno = request.form['invoiceno']
        new_invoicetotal = request.form['invoicetotal']        
        execute_sql('UPDATE invoice SET customername = ?, customeraddress = ?, date = ?, description = ?, invoiceno = ?, invoicetotal = ? WHERE id = ?', 
        new_customername, new_customeraddress, new_date, new_description, new_invoiceno, new_invoicetotal, invoice_id)
        flash('Invoice updated!', category='greenlight')
        return redirect('/viewinvoice')

    # Render edit form with invoice data
    return render_template('editinvoice.html', invoice=invoice)

@app.route('/deleteinvoice/<int:invoice_id>', methods=['POST'])
def deleteinvoice(invoice_id):
    # Connect to database and delete invoice record
    execute_sql('DELETE FROM invoice WHERE id = ?', invoice_id,)
    flash('Invoice deleted!', category='greenlight')
    return redirect('/viewinvoice')  

if __name__ == '__main__':
    # app.secret_key = 'asdasdasd'
     app.run()


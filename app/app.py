# Import Flask module and initialize app
from flask import Flask, render_template, request, flash, redirect
from datetime import datetime
# Import database functions from db_func
from db_func.db_func import get_db, validate_invoice_form, execute_sql, run_query
 


app = Flask(__name__)

# Set secret key for session management
app.config['SECRET_KEY'] = 'your-secret-key'

# Defines route for homepage
@app.route('/',  methods=['GET','POST'])
def home():
    # Render home.html from template
    return render_template("home.html")

# Define route for addinvoice
@app.route('/addinvoice', methods = ['GET', 'POST'])
def addinvoice(): 
    # Check if request is POST, form submitted
    if request.method == 'POST':
        # Get form data from request object
        customername = request.form.get('customername')
        customeraddress = request.form.get('customeraddress')
        date = request.form.get('date')       
        description = request.form.get('desp')
        invoiceno = request.form.get('invoiceno')
        invoicetotal = request.form.get('invoicetotal')
        
        # Validate form data and flash error message if necessary
        error = validate_invoice_form(customername, customeraddress, date, description, invoiceno, invoicetotal)
        if error is not None:
            # Display error message in flash message
            flash(error, category='redlight')
        else:
            # If form data is valid, insert data into database
            execute_sql('INSERT INTO invoice (customername, customeraddress, date, description, invoiceno, invoicetotal) VALUES (?, ?, ?, ?, ?, ?)', 
                        customername, customeraddress, date, description, invoiceno, invoicetotal)
            # Display success message in flash message
            flash('Invoice added!', category='greenlight')
          
    # Render Form.html 
    return render_template("Form.html")

# Define route for viewinvoice
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
        # Retrieve all updated data from the form 
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

    # Render editinvoicea
    return render_template('editinvoice.html', invoice=invoice)

@app.route('/deleteinvoice/<int:invoice_id>', methods=['POST'])
def deleteinvoice(invoice_id):
    # Connect to database and delete invoice record
    execute_sql('DELETE FROM invoice WHERE id = ?', invoice_id,)
    flash('Invoice deleted!', category='greenlight')
    return redirect('/viewinvoice')  

if __name__ == '__main__':
     app.run()


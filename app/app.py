from flask import Flask, Blueprint, render_template, request, flash, redirect
#import sqlite3
from datetime import datetime
#from db_func import *
#import os 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

@app.route('/',  methods=['GET','POST'])
def home():
    return render_template("home.html")


if __name__ == '__main__':
    app.secret_key = 'asdasdasd'
    app.run(debug=True)

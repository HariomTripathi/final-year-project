from flask import Flask, render_template, request, session ,url_for, redirect
import pickle
import numpy as np
import pymysql

app = Flask(__name__)
app.secret_key = "qwerty123"

con = pymysql.connect(host='localhost', port = 3306, user='root', password='Mysql@123', database="whowins")
cur = con.cursor()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/home')
def home():
    return render_template('prediction.html', username = session['username'])

@app.route('/SigninAuthentication', methods=['POST','GET'])
def SigninAuthentication():
    msg = ""
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']

        if username == "" or password == "":
            msg = 'All Fields are required!'
        else:
            cur.execute('select * from accounts where username=%s and password=%s',(username,password))
            row = cur.fetchone()
            if row == None:
                msg = 'Invalid Credentials. Please Try Again!'
            else:
                session['loggedin'] = True
                session['username'] = row[1]
                return redirect(url_for('home'))
    return render_template('index.html',msg)


if __name__ == '__main__':
	app.run(debug=True)

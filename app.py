import random

from flask import Flask, render_template, request, session, redirect, url_for
import pickle
import numpy as np
import os
import pymysql
from twilio.rest import Client

app = Flask(__name__)
app.secret_key = os.urandom(24)

con = pymysql.connect(host='localhost', port=3306, user='root', password='Mysql@123', database="whowins")
cur = con.cursor()


@app.route('/')
def index():
    if 'userid' in session:
        return redirect('/home')
    else:
        return render_template('index.html')


@app.route('/home')
def home():
    if 'userid' in session:
        return render_template('home.html', username=session['username'])
    else:
        return redirect('/')


@app.route('/SigninAuthentication', methods=['POST', 'GET'])
def SigninAuthentication():
    msg = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "" or password == "":
            msg = 'All Fields are required!'
        else:
            cur.execute('select * from accounts where username=%s and password=%s', (username, password))
            row = cur.fetchone()
            if row is None:
                msg = 'Invalid Credentials. Please Try Again!'
            else:
                session['username'] = row[1]
                session['userid'] = row[0]
                session['mobno'] = row[4]
                return redirect('/home')
    return render_template('index.html', msg)


@app.route('/Registration')
def Register():
    return render_template('registration.html')


@app.route('/RegisterAuthentication', methods=['POST', 'GET'])
def RegisterAuthentication():
    msg = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        mobno = request.form['mobno']

        if username == "" or password == "" or email == "":
            msg = 'All Fields are required!'
        else:
            cur.execute("INSERT INTO accounts (username, password, email, mobileno) VALUES (%s,%s,%s,%s)",
                        (username, password, email, mobno))
            con.commit()
            cur.execute('select * from accounts where username=%s and password=%s', (username, password))
            row = cur.fetchone()
            session['username'] = username
            session['userid'] = row[0]
            session['mobno'] = mobno
            return redirect('/home')
    return render_template('index.html', msg)


@app.route('/logout')
def logout():
    session.pop('userid')
    session.pop('username')
    session['loggedin'] = False
    session.pop('mobno')
    return redirect('/')


@app.route('/OtpAuthentication')
def OtpAuthentication():
    if 'userid' in session:
        mobno = session['mobno']
        val = getOTPApi(mobno)
        if val:
            return render_template('getotp.html')
    else:
        return redirect('/')


def getOTPApi(mobno):
    account_sid = 'AC176c49b0ef6b5b8a84fd359c6c3464b1'
    auth_token = '0f1df18a595e3735dadef290473753c3'
    client = Client(account_sid, auth_token)
    otp = random.randrange(100000, 999999)
    session['response'] = str(otp)
    body = 'Your Otp is ' + str(otp)
    message = client.messages.create(
        messaging_service_sid='MGcc756f34d7fc6c331b6eced9137df867',
        body=body,
        to=mobno
    )
    if message.sid:
        return True
    else:
        return False


@app.route('/ValidateOTP', methods=['Post'])
def ValidateOTP():
    otpe = request.form['otpe']
    if 'response' in session:
        otp = session['response']
        session.pop('response', None)
        if otp == otpe:
            session['loggedin'] = True
            return redirect('/home')
        else:
            return redirect('/logout')


if __name__ == '__main__':
    app.run(debug=True)

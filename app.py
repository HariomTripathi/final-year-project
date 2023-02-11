import random
import stripe
from flask import Flask, render_template, request, session, redirect
import os
import pymysql
from twilio.rest import Client
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = os.urandom(24)

stripe.api_key = "sk_test_51MX4FKSAiZcXYUcJevfTY3LWCFU1lotHrq5dabjHZY6Ncpeg7AXxt6jS6vObKZzmYtb9yR9TrFIEFEKD1sON8XRk00mlYpCp8M"

con = pymysql.connect(host='sql12.freesqldatabase.com', port=3306, user='sql12596806', password='Mysql@123', database="sql12596806")
cur = con.cursor()

filename = 'first-innings-score-lr-model.pkl'
regressor = pickle.load(open(filename, 'rb'))


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
            a='0'
            cur.execute("INSERT INTO accounts (username, password, email, mobileno, subscription) VALUES (%s,%s,%s,%s,%s)",(username, password, email, mobno, a))
            con.commit()
            cur.execute('select * from accounts where username=%s and password=%s', (username, password))
            row = cur.fetchone()
            session['username'] = username
            session['userid'] = row[0]
            session['mobno'] = mobno
            return redirect('/home')
    return render_template('index.html', msg)


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
    auth_token = 'b319534b1dbdda4a6c4174183dd12efb'
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


@app.route('/logout')
def logout():
    session.pop('userid')
    session.pop('username')
    session['loggedin'] = False
    session.pop('mobno')
    return redirect('/')


@app.route('/pricing')
def pricing():
    return render_template('pricing.html')


@app.route('/create_checkout_session3m',methods=['POST', 'GET'])
def create_checkout_session3m():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    "price":"price_1MYk82SAiZcXYUcJNVMiac8s",
                    "quantity":1
                }
            ],
            mode="payment",

            success_url= "http://127.0.0.1:5000/amount3m",
            
            cancel_url = "http://127.0.0.1:5500/templates/cancel.html"
        )
    except Exception as e:
        return str(e)
 
    return redirect(checkout_session.url,code=303)
 

@app.route('/amount3m' , methods=['POST','GET'])
def amount3m():
    username = session['username']
    cur.execute('select * from accounts where username=%s',(username) )
    row = cur.fetchone()
    a=row[5]
    if a is None:
        a = 0
    a=int(a)+3
    a=str(a)
    cur.execute('update accounts set subscription=%s where username=%s',(a,username) )
    con.commit()
    return redirect('/')


@app.route('/create_checkout_session6m',methods=['POST', 'GET'])
def create_checkout_session6m():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    "price":"price_1MYkGeSAiZcXYUcJp37OVvgH",
                    "quantity":1
                }
            ],
            mode="payment",
            success_url="http://127.0.0.1:5000/amount6m",
            
            cancel_url = "http://127.0.0.1:5500/templates/cancel.html"
        )
    except Exception as e:
        return str(e)
 
    return redirect(checkout_session.url,code=303)
 

@app.route('/amount6m' , methods=['POST','GET'])
def amount6m():
    username = session['username']
    cur.execute('select * from accounts where username=%s',(username) )
    row = cur.fetchone()
    a=row[5]
    if a is None:
        a = 0
    a=int(a)+6
    a=str(a)
    cur.execute('update accounts set subscription=%s where username=%s',(a,username) )
    con.commit()
    return redirect('/')


@app.route('/create_checkout_session12m',methods=['POST', 'GET'])
def create_checkout_session12m():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    "price":"price_1MYkHoSAiZcXYUcJyN5krHM4",
                    "quantity":1
                }
            ],
            mode="payment",
            success_url="http://127.0.0.1:5000/amount12m",
            
            cancel_url = "http://127.0.0.1:5000/templates/cancel.html"
        )
    except Exception as e:
        return str(e)
 
    return redirect(checkout_session.url,code=303)
 

@app.route('/amount12m' , methods=['POST','GET'])
def amount12m():
    username = session['username']
    cur.execute('select * from accounts where username=%s',(username) )
    row = cur.fetchone()
    a=row[5]
    if a is None:
        a = 0
    a=int(a)+12
    a=str(a)
    cur.execute('update accounts set subscription=%s where username=%s',(a,username) )
    con.commit()
    return redirect('/')


@app.route('/predicthome')
def predicthome():
    return render_template('predicthome.html')


@app.route('/predict', methods=['POST'])
def predict():
    temp_array = list()
    
    if request.method == 'POST':
        
        batting_team = request.form['batting-team']
        if batting_team == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0]
        elif batting_team == 'Delhi Daredevils':
            temp_array = temp_array + [0,1,0,0,0,0,0,0]
        elif batting_team == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,1,0,0,0,0,0]
        elif batting_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,1,0,0,0,0]
        elif batting_team == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,1,0,0,0]
        elif batting_team == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,1,0,0]
        elif batting_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,1,0]
        elif batting_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,1]
            
            
        bowling_team = request.form['bowling-team']
        if bowling_team == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0]
        elif bowling_team == 'Delhi Daredevils':
            temp_array = temp_array + [0,1,0,0,0,0,0,0]
        elif bowling_team == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,1,0,0,0,0,0]
        elif bowling_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,1,0,0,0,0]
        elif bowling_team == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,1,0,0,0]
        elif bowling_team == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,1,0,0]
        elif bowling_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,1,0]
        elif bowling_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,1]
            
            
        overs = float(request.form['overs'])
        runs = int(request.form['runs'])
        wickets = int(request.form['wickets'])
        runs_in_prev_5 = int(request.form['runs_in_prev_5'])
        wickets_in_prev_5 = int(request.form['wickets_in_prev_5'])
        
        temp_array = temp_array + [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]
        
        data = np.array([temp_array])
        my_prediction = int(regressor.predict(data)[0])
              
        return render_template('result.html', lower_limit = my_prediction-10, upper_limit = my_prediction+5)


@app.route('/csk')
def csk():
    return render_template('csk.html')


@app.route('/dc')
def dc():
    return render_template('dc.html')


@app.route('/gt')
def gt():
    return render_template('gt.html')


@app.route('/kkr')
def kkr():
    return render_template('kkr.html')


@app.route('/lsg')
def lsg():
    return render_template('lsg.html')


@app.route('/mi')
def mi():
    return render_template('mi.html')


@app.route('/pk')
def pk():
    return render_template('pk.html')


@app.route('/rcb')
def rcb():
    return render_template('rcb.html')


@app.route('/rr')
def rr():
    return render_template('rr.html')


@app.route('/srh')
def srh():  
    return render_template('srh.html')


if __name__ == '__main__':
    app.run(debug=True)

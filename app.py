from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/SigninAuthentication', methods=['POST','GET'])
def SigninAuthentication():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        
        if (username=='har123' and password=='9653'):
            
            return render_template('prediction.html')
        else:
            return render_template('again.html')


if __name__ == '__main__':
	app.run(debug=True)

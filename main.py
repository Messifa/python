from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
  
app = Flask(__name__)


@app.route('/accueuil')
def base():
    return render_template("base.html")

@app.route('/page se connecter')
def hom():
    return render_template("home.html")

@app.route('/')
def index():
    return render_template("base.html")

@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM idutilisateurs WHERE email = % s AND password = % s', (email, password ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            session["mesage"] = mesage
            return redirect('/page se connecter')
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage=mesage)

@app.route('/signup', methods =['GET', 'POST'])
def signup():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM idutilisateurs WHERE email = % s and password = % s', (email, password))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email, ):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        elif len(password) < 4:
            mesage="password is short"
        else:
            cursor.execute('INSERT INTO idutilisateurs VALUES (NULL, % s, % s, % s)', (userName, email, password, ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('signup.html', mesage=mesage)
    


@app.route('/home')
def home():
    try:
        if(session['id'] == None):
            pass     
    except:
        return redirect("/login")
    return render_template('page se coonecter')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    session.pop('name', None)
    session.pop('mesage', None)
    return redirect("/accueuil")
  


  
  
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user'
  
mysql = MySQL(app)

if __name__ == "__main__":
    app.run(debug=True)
  

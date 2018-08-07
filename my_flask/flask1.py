#!/usr/bin/python2
from flask import Flask,render_template,flash,redirect,url_for ,session,request, logging
from data import Articles
from wtforms import Form,StringField, TextAreaField, PasswordField,validators
#from passlib.hash import sha256_crypt
import mysql.connector as mariadb

conn = mariadb.connect(user='root',host='localhost', password='l', database='MYFLASK')
cur = conn.cursor()


#current case for the module which is (__name__)
#instance of the flask class
app = Flask(__name__)

Articles = Articles()
#/ is the route
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles=Articles)

@app.route('/articles/<string:id>/')
def article(id):
    return render_template('article.html', id=id)

class RegisterForm(Form):
    
    name = StringField('Name',[validators.Length(min=2,max=50)])
    username = StringField('Username',[validators.Length(min=2,max=25)])
    email = StringField('Email',[validators.Length(min=2,max=50)])
    password = PasswordField('Password', [
    
            validators.DataRequired(),
            validators.EqualTo('confirm',message='Passwords dont match')

    ]) 
    confirm = PasswordField('confirm password')

    @app.route('/register',methods=['GET','POST'])
    def register():
        form = RegisterForm(request.form)
        if request.method == 'POST' and form.validate():
            name = form.name.data
            email = form.email.data
            username = form.username.data
            password = form.password.data
            #password = sha256_crypt.encrypt(str(form.password.data))

            cur.execute("INSERT INTO USERS(name,email,username,password) VALUES(%s,%s,%s,%s)", (name,email,username,password))
            conn.commit()
            conn.close()

            flash('You are now registered')
           #return redirect(url_for('index'))
        return render_template('register.html',form=form)



    
    conn = mariadb.connect(user='root',password='l',database='MYFLASK')
    cur = conn.cursor()
 # for user login
    @app.route('/login',methods=['GET','POST'])
    def login():
        if request.method == 'POST':
            #return "hey"
            #getting forms details
            username =  request.form['username']
            #password_candidate =  sha256_crypt.encrypt(str(request.form['password']))
            password_candidate =  request.form['password']
            #password = (password_candidate)
            #return "heuy"
            #GETTING USER BY USER NAME
            result =  cur.execute("SELECT * FROM USERS WHERE username = '11qq' ")
            print result
            #result = cur.execute("SELECT * FROM USERS WHERE username = %s",[username])
            #return "hey"
            #if result[4]==password_candidate:
            if result > 0:
            #return "heyu"
                data = cur.fetchone()
                password = data['password']

            #if result[password] == password_candidate:
            #   return "gd"

            #for row in result:
                #return "heyyyy"    
                #if row[4] == password_candidate:
                   # return "hey"
#            password = data['password']

                #COMPARONG THE PASSWORD GET FOR ANY USER
                if (password_candidate == password):
                #if sha256_crypt.verify(password_candidate,password):
                    session['logged_in'] = True
                    session['username'] = username
                    flash('you are logged in ','success')
                    return redirect(url_for('dashboard'))
                    app.logger.info('PASSWORD MATHCED')
                
                else:
                    error = 'Invalid user'
                    app.logger.info('PAssword font matched up')

            else:
                error = 'username not found'
                return render_template('login.html',error=error)

        return render_template('login.html')
        conn.close()

    @app.route('/dashboard')
    def dashboard():
        return 'hey sexy'


#   below mean that the script is being executed
#here debug=true is to run the server again
if __name__=='__main__': 
    app.secret_key='secret123'
    app.run(debug=True) 

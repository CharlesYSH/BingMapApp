import time, os
import httplib2
import hashlib
import argparse
from flask import Flask, render_template, flash, request, redirect, url_for, session, send_from_directory
from flask_session import Session
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import sqlite3
import path_Generation as pg

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = b"\xec\x13F\x90_\x0c\xe7MEL\xf6.B\xe7\x1f\xa0'\x8d\xf5E-\x0c\xb0@\x9d\x06\xe9\xc9$o7\xd0"
app.config['SESSION_TYPE'] = 'filesystem'
sess = Session()
sess.init_app(app)


class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])  
 
@app.route("/login", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    if not form:
        print (form.errors)
        
    if request.method == 'POST':
        connectdb = sqlite3.connect('test.db')
        c = connectdb.cursor()
        name=request.form['name']
        password=request.form['password']
        #print (name,password)
        if form.validate():
            #sheet = connect_login_sheet()
            #if ([name] in sheet) and compare_sheet_PW(sheet.index([name]),password):
            sqlCMD = "SELECT id,name,password FROM loginfo WHERE name='%s' AND password='%s'"%(name,md5(password))
            if(c.execute(sqlCMD).fetchall()):
                flash('Nice to meet you back.')
                session['username'] = name
                return redirect(url_for('search'))
            else:
                flash('Error: The name or password you’ve entered is incorrect.')
        else:
            flash('Error: All the form fields are required. ')
        
    return render_template('hello.html', form=form)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/", methods=['GET', 'POST'])
def search():
#    if not session.get('username'):
#        return redirect(url_for('hello'))
    return render_template('search.html', form=Form)

@app.route('/navigation', methods=['GET', 'POST'])
def navigation():
#    if not session.get('username'):
#        return redirect(url_for('hello'))
    return render_template('navigation.html', form=Form)

@app.route('/about', methods=['GET', 'POST'])
def profile():
#    if not session.get('username'):
#        return redirect(url_for('hello'))
    return render_template('about.html', form=Form)
    
@app.route('/trip', methods=['GET', 'POST'])
def trip():
#    if not session.get('username'):
#        return redirect(url_for('hello'))
    path,address = pg.path_Generation()
    return render_template('trip.html', geocode=path, address=address,form=Form)
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('_flashes', None)
    flash('You were logged out.')
    return redirect(url_for('hello'))

def md5(text):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=DEBUG)

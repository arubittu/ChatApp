import os
import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session,url_for
from flask_socketio import SocketIO,send,emit

# Configure application
app= Flask(__name__)
socketio=SocketIO(app)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True #?
app.config['SECRET_KEY']='secret!'
# Configure CS50 Library to use SQLite database
 
connected=[] #people online


#make data base of people who have logged in
#connection=sqlite3.connect('people.db')
#cursor=connection.cursor()
#command1="""CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)"""
#cursor.execute(command1)



@app.route('/')
def signup():
    return render_template('signup.html')



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        with sqlite3.connect('people.db') as connection:
            cursor=connection.cursor()
            cursor.execute("INSERT INTO users (username,password) VALUES(?,?)",(username,password))
            connection.commit()

    return render_template('login.html') 




@app.route('/chat',methods=['GET','POST'])
def chat():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        with sqlite3.connect('people.db') as connection:
            cursor=connection.cursor()
            cursor.execute("""SELECT username,password FROM users WHERE username=? AND password=?""",(username,password))
            result=cursor.fetchone()
            if result:
                session['username']=username
                return render_template('chat.html',username=session['username'])
            else:
                return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))




@socketio.on('person')
def handle_person_event(data):
    print(data['username'])
    socketio.emit('person_connected',data['username'])




@socketio.on('send_msg')
def handle_msgs(data):
    print(data['message'])
    socketio.emit('received_msg',data)


@socketio.on('message')
def send_connected(data):
    connected.append(data)
    socketio.emit('online',connected)


@socketio.on('delete')
def delete_user(data):
    connected.remove(data.username)
    print('\n\n{}'.format(data.username))
    socketio.emit('online',connected)





if __name__=='__main__':
    socketio.run(app,debug=True)
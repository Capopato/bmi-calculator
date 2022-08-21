from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy  # import database

app = Flask (__name__)
app.secret_key = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'   # import config setup database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Turn of tracking of all modifications (can cause errors)
app.permanent_session_lifetime = timedelta (hours=5)

db = SQLAlchemy(app)


class users(db.Model):  # Create a class with db.ModeL in it so it knows its a database
    _id = db.Column(db.Integer, primary_key=True)  # Create a column for ID's + primary_key so that everything has it's own unique key
    name = db.Column(db.String(100))  # standard sentence to set data
    email = db.Column(db.String(100))
    """gender = db.Column(db.String(100))
    age = db.Column(db.Integer())
    height = db.Column(db.Integer())
    weight = db.Column(db.Integer())"""


    def __init__(self, name, email, gender, age, height, weight):
        self.name = name
        self.email = email
        self.gender = gender
        self.age = age
        self.height = height
        self.weight = weight


@app.route ('/home')
@app.route ('/')
def home ():
    return render_template ("bmi-calculator.html")


@app.route('/view')
def view():
    return render_template('view.html', values=users.query.all())


@app.route ('/login', methods=['POST', "GET"])  # Post = secured, POST = unsecured data
def login ():
    if request.method == 'POST':  # If request == POST then take the data and secure it
        session.permanent = True
        user = request.form['username']  # Make a variable and assign it to the name of the input in the login.html
        session['user'] = user

        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session['email'] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()
        flash('Login succesfull')
        return redirect (url_for ('user'))  # redirect the data to the other user page
    else:  # If request == /login aka Get > just take it to the website
        if 'user' in session:
            flash('Already logged in')
            return redirect (url_for ('user'))

        return render_template ('login.html')


  #TODO: create all the entries for the data and store it correctly in the database
  #TODO: Insert the formula to the data and store the answer in the database
  #TODO: Display the answer on the same page below the data entry points
  #TODO: Make valid link to bmi-calculator


@app.route ('/bmi-calculator', methods=['POST', "GET"])
def user ():
    email = None
    if 'user' in session:
        user = session['user']

        if request.method == 'POST':
            email = request.form["email"]
            session['email'] = email
            found_user = users.query.filter_by (name=user).first ()
            found_user.email = email
            db.session.commit()
            flash('Information saved')
        else:
            if ('email' in session):
                email = session['email']
        return render_template('bmi-calculator.html')
    else:
        flash('You are not logged in')
        return redirect (url_for ('login'))


@app.route ('/logout')
def logout ():
    flash('Log out succesfull', 'info')
    session.pop ('user', None)
    session.pop ('email', None)
    return redirect (url_for ('login'))


if __name__ == '__main__':
    db.create_all()
    app.run(host="localhost", port=8000, debug=True)
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
import settings
app = Flask(__name__)

def mysql_raw_connection():
    """
        Used for connecting with mysql database if not using SQLAlchemy can go with 
        these function
    """
    app.config['MYSQL_HOST'] = settings.mysql_host
    app.config['MYSQL_USER'] = settings.mysql_user
    app.config['MYSQL_PASSWORD'] = settings.mysql_pwd
    app.config['MYSQL_DB'] = settings.mysql_db
    app.config['MYSQL_PORT'] = settings.mysql_port
    return(1)

# mysql_raw_connection()
# def create_tables():
#     """
#         if we are using raw mysql instead of sqlalchemy we are using these to create table
#     """
#     with app.app_context():
#         mysql = MySQL(app)
#         cur = mysql.connection.cursor()
#         cur = mysql.connection.cursor()
#         cur.execute("DROP TABLE IF EXISTS raw_query_user_table")
#         cur.execute("CREATE TABLE raw_query_user_table (name VARCHAR(255), address VARCHAR(255))")
#         mysql.connection.commit()
#         cur.close()
# create_tables()

def mysql_alchemy():
    """
        These function used to link sql alchemy with the database
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{0}:{1}@{2}/{3}'.format(settings.mysql_user,settings.mysql_pwd,settings.mysql_host,settings.mysql_db)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    return  SQLAlchemy(app)

db = mysql_alchemy()


#Implementation of monolithic application
class User(db.Model):
    """
        Basic User table with username and password
    """
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True)
    password = db.Column(db.String(30), unique = True)

    def __repr__(self):
        return "<User {0}>".format(self.username)

class UserDetails(db.Model):
    """
        Basic user details table
    """
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30),nullable=False)
    qualification = db.Column(db.String(30),nullable=False)
    home_address = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(200),nullable=False)

    def __repr__(self):
        return "<User {0} {1}>".format(self.first_name, self.last_name)

@app.before_first_request
def setup_users():
    """
        Before starting first request these function comes into picture
    """
    db.create_all()
    if not User.query.first():
        user = User()
        user.username = 'admin'
        user.password = 'admin'
        db.session.add(user)
        db.session.commit()


@app.route('/', methods = ['GET', 'POST'])
def default_landing_page():
    """
        Landing page function where GET and POST methods are calling and Using index.html page 
        and taking input from user and saving to database use SQL Alchemy
    """
    if request.method == 'POST':
        try:
            usr = request.form['username']
            pwd = request.form['password']
            if usr and pwd :
                user = User()
                user.username = usr
                user.password = pwd
                db.session.add(user)
                db.session.commit()
                return render_template('landing_page.html',error='Added to Database successfully')
            return render_template('landing_page.html',error='Fields username and password mandatory')
        except Exception as e:
            return render_template('landing_page.html',error='Error {0}'.format(e))
    elif request.method == 'GET':
        return render_template('landing_page.html',error='')

@app.route('/user_table/sqlAlchemy/', methods = ['GET'])
def user_table_get_function():
    """
        These function is used to post the data to user_table table taking data from front-end
    """
    if request.method == 'GET':
        query = User.query.all()
        return render_template('user_table.html',users_info=query)


@app.route('/user_table/sqlAlchemy/<pk>/', methods = ['POST'])
def user_table_delete_function(pk):
    """
        These function is used to delete user from the  user_table table taking data from front-end
    """
    if request.method == 'POST':
        user = User.query.get(pk)
        db.session.delete(user)
        db.session.commit()
        query = User.query.all()
        return render_template('user_table.html',users_info=query)
    else:
        query = User.query.all()
        return render_template('user_table.html',users_info=query)


@app.route('/user_details/sqlAlchemy/', methods = ['GET','POST'])
def user_details_table_post_function():
    """
        These function is used to post the data to UserDetails table taking data from front-end
    """
    
    if request.method == 'POST':
        try:
            #taking data from html page
            fname = request.form['first_name']
            lname = request.form['last_name']
            email = request.form['email']
            qualification = request.form['qualification']
            home_address = request.form['home_address']
            # storing data to an object using sqlalchemy
            userDetails = UserDetails()
            userDetails.first_name = fname
            userDetails.last_name = lname
            userDetails.qualification = qualification
            userDetails.home_address = home_address
            userDetails.email = email
            db.session.add(userDetails)
            db.session.commit()
            query = UserDetails.query.all()[::-1]
            return render_template('user_details.html',error='Added successfully',users_info=query)
        except Exception as e:
            query = UserDetails.query.all()[::-1]
            return render_template('user_details.html',error='Error {0}'.format(e),users_info=query)
    else:
        query = UserDetails.query.all()[::-1]
        return render_template('user_details.html',error='',users_info=query)


#implementation Microservices application

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
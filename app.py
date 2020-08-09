from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# app.config['MYSQL_HOST'] = '127.0.0.1'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'flask_test'
# app.config['MYSQL_PORT'] = 3306
# app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1/flask_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True)
    password = db.Column(db.String(30), unique = True)


    def __repr__(self):
        return "<User {0}>".format(self.username)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(200))
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))

    # def __repr__(self):
    #     return "<User {0} {1}>".format(self.first_name, self.last_name)

@app.before_first_request
def setup_users():
    db.create_all()

    if not User.query.first():
        user = User()
        user.username = 'admin'
        user.password = 'admin'
        db.session.add(user)
        db.session.commit()

# def create_tables():
#     with app.app_context():
#         mysql = MySQL(app)
#         cur = mysql.connection.cursor()
#         cur = mysql.connection.cursor()
#         cur.execute("DROP TABLE IF EXISTS customers")
#         cur.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
#         mysql.connection.commit()
#         cur.close()
# create_tables()

@app.route('/', methods = ['GET', 'POST'])
def hello():
    if request.method == 'POST':
        content = request.form['username']
        return "IN POST METHOD"
    elif request.method == 'GET':
        return render_template('index.html')

@app.route('/dashboard/', methods = ['GET'])
def dashboard():
    if request.method == 'GET':
        return render_template('dashboard.html')


@app.route('/dashboard/sqlAlchemy/', methods = ['GET','POST'])
def dashboard_alchemy():
    if request.method == 'POST':
            cust = Customer()
            cust.first_name = "FIRST NAME"
            cust.last_name = "LAST NAME"
            cust.email = "vijay015125@gmail.com"
            cust.username = "Vijay"
            cust.password = "PASS"
            db.session.add(cust)
            db.session.commit()
            return("RECORDED")
        return render_template('index.html')
    elif request.method == 'GET':
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
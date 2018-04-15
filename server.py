from flask import Flask, render_template, redirect, request
# import the function connectToMySQL from the file mysqlconnection.py
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
# invoke the connectToMySQL function and pass it the name of the database we're using
# connectToMySQL returns an instance of MySQLConnection, which we will store in the variable 'mysql'
mysql = connectToMySQL('usersdb')
# now, we may invoke the query_db method


#--------------------
#   render index.html
#---------------------
@app.route('/')
def index():
    query = "SELECT * FROM users"
    all_users = mysql.query_db(query)
    return render_template('index.html', users = all_users)
#--------------------
#   render show.html
#---------------------
@app.route('/users/<id>', methods=['GET'])
def show(id):
    query = "SELECT * FROM users where id = {}".format(id)
    all_users = mysql.query_db(query)
    return render_template('show.html', users = all_users)
#--------------------
#   render new.html
#---------------------
@app.route('/users/new', methods=['GET'])
def add_new():
    
    return render_template('new.html')
#--------------------
# RENDER edit.html
#--------------------
@app.route('/users/<id>/edit', methods=['GET'])
def edit(id):
    print(id)
    query = "SELECT * FROM users where id = {}".format(id)
    all_users = mysql.query_db(query)
    print(all_users)
    return render_template('edit.html', users = all_users)
#------------------------
# ADD A NEW USER
#------------------------
@app.route('/users', methods=['POST'])
def create():    
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW());"
    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'email': request.form['email']
           }
    mysql.query_db(query, data)
    return redirect('/')
#------------------------
# UPDATE USER INFORMATION
#------------------------
@app.route('/update/<id>', methods=['POST'])
def update(id):
    query = "UPDATE users SET users.first_name = '{}', users.last_name= '{}', users.email= '{}' WHERE id = {}".format(request.form['first_name'], request.form['last_name'], request.form['email'], id)
    mystuff = mysql.query_db(query)
    return redirect('/')
#-----------------------------
# DELETE USER FROM DATA TABLE
#-----------------------------
@app.route('/destroy/<id>', methods=['POST', 'GET'])
def delete(id):
    print(id)
    query = "DELETE FROM users WHERE id ={}".format(id)
    mysql.query_db(query)
    return redirect('/')
@app.route('/users/destroy/<id>', methods=['POST', 'GET'])
def editdelete(id):
    print(id)
    query = "DELETE FROM users WHERE id ={}".format(id)
    mysql.query_db(query)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

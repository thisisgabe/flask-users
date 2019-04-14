from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL

app = Flask(__name__)

@app.route('/')
def root():
    return redirect('/users')

@app.route('/users')
def users():
    mysql = connectToMySQL("flask_users")
    users = mysql.query_db("SELECT * FROM users WHERE deleted IS NULL;")
    print(users)
    return render_template("users.html", user_data = { 'user_list': users })

@app.route('/users/<id>')
def user(id):
    mysql = connectToMySQL("flask_users")
    query = "SELECT * FROM users WHERE id = %(id)s AND deleted IS NULL;"
    data = {
        "id": id
    }
    user_results = mysql.query_db(query, data)
    print(user_results[0])
    return render_template("user_detail.html", user = user_results[0])

@app.route('/users/<id>/edit')
def user_edit(id):
    mysql = connectToMySQL("flask_users")
    query = "SELECT * FROM users WHERE id = %(id)s AND deleted IS NULL;"
    data = {
        "id": id
    }
    user_results = mysql.query_db(query, data)
    print(user_results[0])
    return render_template("edit_user.html", user = user_results[0])

@app.route('/users/new')
def new_user():
    return render_template("add_user.html")

@app.route("/users/create", methods=["POST"])
def add_user_to_db():
    print(request.form)
    # QUERY: INSERT INTO first_flask (first_name, last_name, occupation, created_at, updated_at) 
    #                         VALUES (fname from form, lname from form, occupation from form, NOW(), NOW());
    
    query = "INSERT INTO users (first_name, last_name, email_address) VALUES (%(fname)s, %(lname)s,%(email)s);"
    data = {
        "fname": request.form["fname"],
        "lname": request.form["lname"],
        "email": request.form["email"]
    }
    mysql = connectToMySQL("flask_users")
    user_id = mysql.query_db(query, data)
    return redirect('/users/' + str(user_id))

@app.route("/users/<id>/update", methods=["POST"])
def update_user_on_db(id):
    print(request.form)
    # QUERY: INSERT INTO first_flask (first_name, last_name, occupation, created_at, updated_at) 
    #                         VALUES (fname from form, lname from form, occupation from form, NOW(), NOW());
    
    query = """UPDATE users 
                SET first_name = %(fname)s, last_name = %(lname)s, email_address = %(email)s 
                WHERE id = %(id)s;"""
    data = {
        "fname": request.form["fname"],
        "lname": request.form["lname"],
        "email": request.form["email"],
        "id": id
    }
    mysql = connectToMySQL("flask_users")
    mysql.query_db(query, data)
    return redirect('/users/' + str(data["id"]))

@app.route("/users/<id>/destroy")
def del_user_on_db(id):
    query = """UPDATE users 
                SET deleted = NOW() 
                WHERE id = %(id)s;"""
    data = {
        "id": id
    }
    mysql = connectToMySQL("flask_users")
    mysql.query_db(query, data)
    return redirect('/users')

if __name__=="__main__":
    app.run(debug=True)
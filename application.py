from flask import Flask, render_template, request, jsonify, make_response, session, redirect
from bot2 import chat
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cfbb4b69fa8d88c771ac21dc331c80d377efacbb'

client = MongoClient('mongodb+srv://infobee:InfoBee123@diseaseprediction.e1ihw.mongodb.net/myFirstDatabase'
                     '?retryWrites=true&w=majority')


@app.route('/guestmode', methods=['POST', 'GET'])
def guestmode():
    session['user'] = 'guest'
    if request.method == "POST":
        return render_template("index2.html", guest=0)
    return render_template("index2.html", guest=0)


@app.route('/dashboard')
def dashoard():
    db = client.get_database('diseasepred')
    collection = db.user_record
    record = list()
    for i in collection.find():
        record.append(i)

    db = client.get_database('diseasepred')
    collection = db.user
    users = list()
    for i in collection.find():
        users.append(i)

    return render_template("index.html", record=record, users=users)


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST', 'GET'])
def indexpage():
    try:
        if session['user'] == 'guest':
            session.pop('user')
            return redirect('/signin')
    except:
        pass

    if 'user' not in session:
        return redirect('/signin')
    if request.method == "POST":
        return render_template("index2.html")
    return render_template("index2.html")


@app.route("/entry", methods=['POST', 'GET'])
def entry():
    req = request.get_json()
    print(req)
    res = make_response(jsonify({"name": "{}.".format(chat(req)), "message": "OK"}), 200)
    return res


@app.route('/signin')
@app.route('/signin', methods=['POST', 'GET'])
def login():
    if 'user' in session:
        return redirect('/')
    if request.method == 'POST':
        username = request.form.get('email')
        password = request.form.get('password')
        if username == 'admin@gmail.com' and password == 'admin':
            return redirect('/dashboard')

        if username and password is not None:
            db = client.get_database('diseasepred')
            collection = db.user
            for i in collection.find():
                if i['email'] == username:
                    if i['password'] == password:
                        session['user'] = i['username']
                        return redirect('/')
    return render_template('signin.html')


"""
    This route is for Signup to create new account
"""


@app.route('/signup')
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if 'user' in session:
        return redirect('/')

    if request.method == 'POST':
        username = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        re_password = request.form.get('re_password')

        if username and password is not None:
            db = client.get_database('diseasepred')
            collection = db.user
            for i in collection.find():
                if i['email'] == email:
                    return redirect('/')

        if username and password is not None and password == re_password:
            db = client.get_database('diseasepred')
            collection = db.user
            user_record = {
                'username': username,
                'email': email,
                'password': password,
                're_password': re_password
            }
            collection.insert_one(user_record)
            return redirect('/signin')

    return render_template('signup.html')


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect('/signin')


if __name__ == '__main__':
    app.run(debug=True)

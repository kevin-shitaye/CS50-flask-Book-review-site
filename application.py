from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import or_


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bglupbkmkcgrot:b0680f8dbfbadfe46ce320899aa6f6dd9f2d3f54fb750889c525d492c0710d6c@ec2-52-202-146-43.compute-1.amazonaws.com:5432/dd4jfcjma8pl13'
db = SQLAlchemy(app)


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    logged_in = db.Column(db.Boolean, default=0)

    def __init__(self, username, email, password):
        self.username = username
        self.password = password
        self.email = email


class Books(db.Model):
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.String(4))

    def __init__(self, isbn, title, author, year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year


@app.route('/')
def index():
    # For giving different greetings based on the time
    time = datetime.now()
    greetings = ""
    if time.hour in range(5, 12):
        greetings = "Good morning"
    elif time.hour in range(12, 17):
        greetings = "Good afternoon"
    elif time.hour in range(17, 5):
        greetings = "Good evening"

    return render_template("index.html", greetings=greetings)


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    return render_template("sign_in.html")


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = Users(username=username, email=email, password=password)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/sign_in')
        except:
            return "Unable to register"
    else:
        return render_template("sign_up.html")


@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        tag = request.form['search']
        search = "%{}%".format(tag)
        book_list = Books.query.filter(or_(Books.title.ilike(search), Books.author.ilike(search), Books.isbn.ilike(search)))

    else:
        book_list = Books.query.all()
    return render_template('books.html', book_list=book_list)


if __name__ == "__main__":
    app.run(debug=True)



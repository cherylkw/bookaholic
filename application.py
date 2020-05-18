import os
import requests

from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request,session, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

os.environ['DATABASE_URL'] = "postgres://wzmsxnmxhimbti:42f5f38c438e9a98736225ebb95406a619dc18905848baa85a6d36007309090d@ec2-54-221-217-204.compute-1.amazonaws.com:5432/d843culpiqt63t" 

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Homepage
@app.route("/")
def index():
    return render_template("index.html")

# Member Login
@app.route("/login",methods=["POST"])
def login():
    # check if both usename and password has entered.
    errmsg = "Please enter"
    username = request.form.get("username")
    password = request.form.get("password")
    
    #check if both fields are not empty
    if len(username) is 0 or len(password) is 0:
        if len(username) is 0:
            errmsg = errmsg+" user name . "
        if len(password) is 0:
            errmsg = errmsg+" password!"
        return render_template("index.html", message=errmsg)
    else:
        # if fields are not empty, check enter correct login info.
        member = db.execute("SELECT * FROM members WHERE username = :username", 
        {"username": username}).fetchone()
        if member is None:
            return render_template("index.html", message="Member not exist!")
        else:
            if not check_password_hash(member.password, password):
                return render_template("index.html", message="Wrong password!")
            else:
                session["user_id"] = member.id
                session["username"] = username
                return render_template("search.html")

@app.route("/logout")
def logout():
    try:
        session.pop("user_id")
        session.pop("username")
    except KeyError:
        return render_template("index.html", message="Please Login First")
    return render_template("index.html", message="Logout success!")

# Register an account.
@app.route("/register",methods=["GET", "POST"])
def register():
    # Make sure all fields are entered.
    errmsg = "Please enter"
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        sessionuser = username
        if len(username) is 0 or len(password) is 0: #check if both fields are not empty
            if len(username) is 0:
                errmsg = errmsg+" user name . "
            if len(password) is 0:
                errmsg = errmsg+" password!"
            return render_template("register.html", message=errmsg)
        else:
            # Make sure no duplicated username.
            member = db.execute("SELECT * FROM members WHERE username = :username", {"username": username}).fetchone()
            if member is None:
                try:
                    db.execute("INSERT INTO members (username, password) VALUES (:username, :password)",
                            {"username": username, "password": generate_password_hash(password)})
                    db.commit()
                    return render_template("index.html", message="New account registered! Please login here.")
                except Exception as exc:
                    return render_template("error.html", message=exc)
            else:
                return render_template("register.html",message="The member already exist!")

# Search a book.
@app.route("/search",methods=["GET", "POST"])
def search():
    # Check if one is login.
    if "user_id" not in session:
        return render_template("index.html", message="Please Login First")

    if request.method == "GET":
        return render_template("search.html")
    if request.method == "POST":
        isbn = request.form.get("isbn")
        title = request.form.get("title")
        author = request.form.get("author")
        # Create search query base on criteria.
        if len(isbn) is 0 and len(title) is 0 and len(author) is 0 :
            return render_template("search.html",message="Please enter one of the information to search a book!")
        elif len(isbn) > 0:
            book = db.execute("SELECT * FROM books where upper(isbn) like upper(('%' || :isbn || '%'))", {"isbn" : isbn}).fetchall()
        elif len(title) > 0:
            book = db.execute("SELECT * FROM books where upper(title) like upper(('%' || :title || '%'))", {"title" : title}).fetchall()
        elif len(author) > 0:
            print(author)
            book = db.execute("SELECT * FROM books where upper(author) like upper(('%' || :author || '%'))", {"author" : author}).fetchall()
        if not book:
            return render_template("search.html",message="No match! Search again!")
        else:
            return render_template("lists.html",books=book)

@app.route("/book/<int:book_id>",methods=["GET","POST"])
def book(book_id):
    # Check if one is login.
    if "user_id" not in session:
        return render_template("index.html", message="Please Login First")

    message = ""
    # Add reader review.
    if request.method == "POST":
        user_id = session["user_id"]
        book_id = book_id
        # Make Sure each reader can only add one review.
        if db.execute("SELECT * FROM reviews WHERE members_id = :members_id AND books_id = :books_id", {"members_id": user_id, "books_id": book_id}).rowcount==0:
            comment = request.form.get("comment")
            rating = int(request.form.get("rating"))
            try:
                db.execute("INSERT INTO reviews (comment,rating,members_id,books_id) VALUES (:comment,:rating,:members_id,:books_id)",
                            {"comment": comment, "rating" : rating, "members_id" : user_id, "books_id" : book_id})
                db.commit()
            except Exception as exc:
                return render_template("error.html", message=exc)
        else:
            message="You can only add 1 review for each book."
    
    # Make sure book exists.
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    
    reviews = db.execute("SELECT *, username FROM reviews JOIN members ON members.id = members_id where books_id = :book_id ",{"book_id": book_id}).fetchall()
    if book is None:
        return render_template("error.html", message="No such book.")
    else:
        # Call good reads API to get info.
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "psRI1jX4NUVrywvyMBGoA", "isbns": book.isbn})
        goodbook = res.json()
        return render_template("book.html", book=book, reviews=reviews, goodbook=goodbook, message=message)

# Books API.
@app.route("/api/<string:isbn>", methods=["GET"])
def book_api(isbn):

    # Make sure ISBN exists.
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn",{"isbn":isbn}).fetchone()
    if book is None:
        return jsonify({"error": "Invalid ISBN"}), 404
    else:
        if db.execute("SELECT * FROM reviews WHERE books_id= :books_id",{"books_id": book.id}).rowcount==0:
            total_count = 0
            avg_score = 0
        else:
            reviews = db.execute("SELECT COUNT(rating) AS total_count, SUM(rating) AS total_score FROM reviews WHERE books_id = :books_id GROUP BY books_id",
                        {"books_id": book.id}).fetchall()
            total_count = reviews[0].total_count
            avg_score = reviews[0].total_score / reviews[0].total_count

        # Get book info.
        return jsonify({
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "isbn": book.isbn,
            "review_count": total_count,
            "average_score": avg_score
            })
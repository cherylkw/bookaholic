import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

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


@app.route("/")
def index():
      db.execute("CREATE TABLE books (id SERIAL PRIMARY KEY,isbn VARCHAR NOT NULL,title VARCHAR NOT NULL,author VARCHAR NOT NULL,year VARCHAR NOT NULL)")
      db.execute("CREATE TABLE members (id SERIAL PRIMARY KEY,username VARCHAR NOT NULL,password VARCHAR NOT NULL)")
      db.execute("CREATE TABLE reviews (id SERIAL PRIMARY KEY,comment VARCHAR NOT NULL, rating INTEGER NOT NULL, members_id INTEGER REFERENCES members, books_id INTEGER REFERENCES books)")
      db.commit()
      return "Tables are created"
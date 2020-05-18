# Project 1

Web Programming with Python and JavaScript

**Weclome to Bookaholic**

It's a project about search for books information and reviews. User can perform below action in this book review system called "Bookaholic"
1. Register as a member
2. Login to system
3. Search books base on ISBN / Title / Author
4. Display Goodreads reviews info (total score and average rate) by reading **Goodreads API**
5. Add your own book review on the system
6. Retrieve the book info
7. Create an **API** which allow other apps to retrieve Bookaholic book reviews in **JSON** format
7. Logout

## Added value :
1. Responsive web design
2. Password hash
3. Error checking on each page, ensure all data entered correctly

## Functions functionality in application.py:
index() : Homepage
login() : Get the username and password to login to system, session("user_id") and session("username") is being stored in this function
register() : Add member onto system
logout() : Logout system by clearing session variables
search() : retrieve book list by entered criteria
book() : retrieve individual book info and reviews from system, also using Goodreads API to retrieve their book reviews info
book_api() : an api which allow other apps to retrieve our book reviews info from our system (JSON)


## HTML :
book.html : Display individual book info
error.html : call when having server error
index.html : homepage
layout.html : layout for all html
lists.html : Display book list after searched
register.html : Member register page
search.html : search book page 
create.py : create all tables 
import.py : import data from bookscsv to database

## Youtube Demo :

https://www.youtube.com/watch?v=A2wfYVgHJGU

## Pre-requisites and programs used versions

-  Python 3.6 or higher
-  the latest version of pip

## Setting up the development environment

1. git clone this project

2. Run **pip3 install -r requirements.txt** in your terminal window to make sure that all of the necessary Python packages (Flask and Flask-SocketIO, for instance) are installed.

3. Set the environment variable **FLASK_APP** to be application.py. On a Mac or on Linux, the command to do this is export FLASK_APP=application.py. On Windows, the command is instead set FLASK_APP=application.py.

4. Run flask run to start up your Flask application.

## Visiting an URL and interact with the application

- Open the localhost http://127.0.0.1:5000/ to run the app

Author : Cheryl Kwong Email : cherylkwong@gmail.com

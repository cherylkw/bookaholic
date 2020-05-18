# Bookaholic

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

## Setting up PostgreSQL Database

This project is using PostgreSQL database hosted by Heroku, so make sure you have registered an account in Heroku and connect the DB.

1. On Heroku’s Dashboard, click “New” and choose “Create new app.”
2. Give your app a name, and click “Create app.”
3. On your app’s “Overview” page, click the “Configure Add-ons” button.
4. In the “Add-ons” section of the page, type in and select “Heroku Postgres.”
5. Choose the “Hobby Dev - Free” plan, which will give you access to a free PostgreSQL database that will support up to 10,000 rows of data. Click “Provision.”
6. Click the “Heroku Postgres :: Database” link.
7. You should now be on your database’s overview page. Click on “Settings”, and then “View Credentials.” This is the information you’ll need to log into your database. You can access the database via Adminer, filling in the server (the “Host” in the credentials list), your username (the “User”), your password, and the name of the database, all of which you can find on the Heroku credentials page.

## Visiting an URL and interact with the application

- Open the localhost http://127.0.0.1:5000/ to run the app

Author : Cheryl Kwong Email : cherylkwong@gmail.com

Developed by Python, Flask, HTML,PostgreSQL,Heroku

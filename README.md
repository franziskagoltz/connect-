[![Build Status](https://travis-ci.org/franziskagoltz/connect_plusplus.svg?branch=master)](https://travis-ci.org/franziskagoltz/connect_plusplus)

<h2>Connect++</h2>
<h3>A Smart Connections Manager</h3>

<h3>Overview:</h3>
Connect++ is a smart connections manager, that allows the user to keep track of their connections: where do they live? what is their contact information? what are their interests?


<h4>Technology Stack:</h4>

Python, Flask, Flask Bcrypt, PostgreSQL, SQLAlchemy, JavaScript (AJAX, JSON, jQuery), HTML, Jinja, CSS, Bootstrap, 
Tests: Python Unit Tests, Travis CI


<h4>APIs Used:</h4>

Facebook Oauth


![Connect++](/static/imgs/readme-imgs/connect++-home.png)


<h4>How it works</h4>

A user can sign up directly on the site or login via facebook:

![Connect++](/static/imgs/readme-imgs/login.gif)

<h4>Features:</h4>

A user can add a new connection to their network

![Connect++](/static/imgs/readme-imgs/add-connection.gif)


A user can see their connections and filter by city, clicking on the connection
allows the user to see all detail 

![Connect++](/static/imgs/readme-imgs/view-filter.gif)


A user can edit information about their connections

![Connect++](/static/imgs/readme-imgs/edit.gif)


A user can also search for connections matching any part of their name

![Connect++](/static/imgs/readme-imgs/search.gif)

<h4>Tests:</h4>

Connect++ has 91% test coverage in Python
![Tests++](/static/imgs/readme-imgs/coverage)
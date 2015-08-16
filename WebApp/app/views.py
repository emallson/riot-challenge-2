from flask import render_template, flash, redirect, g, request
from app import app
from .forms import LoginForm
from werkzeug.local import LocalProxy
couch = LocalProxy(lambda: g.couch)

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Impally'}  # fake user
	return render_template('index.html', 
							title='Home',
							user=user)

@app.route('/view_profile')
def view_profile():
	document = couch.get("25023dc39a5f00c52fb91eb35b000e91")
	return "This works!"
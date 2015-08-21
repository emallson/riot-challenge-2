from flask import render_template, flash, redirect, g, request
from app import app
from werkzeug.local import LocalProxy
couch = LocalProxy(lambda: g.couch)

def getChampName(champID):
	champion_name_view = ViewDefinition('champions', 'champName', '''\
              function(doc) 
                      { 
                        Object.keys(doc).forEach(function(k) 
                          { emit(k, doc[k].name); }); }"
		''')
	manager.add_viewdef(champion_name_view)
	champKeys = champion_name_view()
	return champKeys[1]

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
	return getChampName(1)
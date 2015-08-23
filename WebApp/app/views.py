from flask import render_template, flash, redirect, g, request
from app import app
import couchdb
from flaskext.couchdb import CouchDBManager, ViewDefinition
from werkzeug.local import LocalProxy
couch = LocalProxy(lambda: g.couch)

manager = CouchDBManager()

def getChampInfo(champID):
	champion_name_view = ViewDefinition('app', 'champName', "function(doc) { Object.keys(doc.data).forEach(function(k) { emit(k, doc.data[k].image); }); }")
	manager.add_viewdef(champion_name_view)
	champKeys = champion_name_view[champID]
	
	for champ in champKeys: return(champ.key)

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Impally'}  # fake user
	return render_template('index.html', 
							title='Home',
							user=user)

@app.route('/view_profile')
def view_profile():
	return getChampInfo('Zac')
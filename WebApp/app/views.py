from flask import render_template, flash, redirect, g, request
from app import app
import couchdb
from flaskext.couchdb import CouchDBManager, ViewDefinition
from werkzeug.local import LocalProxy
couch = LocalProxy(lambda: g.couch)

manager = CouchDBManager()
list_view = ViewDefinition('app', 'dataList', "function(doc) { Object.keys(doc.data).forEach(function(k) { emit(k, doc.data[k]); }); }")
manager.add_viewdef(list_view)


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/Champions')
def Champions():
	champList = list_view["a":"Z"]
	champions = champList[:]
	return render_template('insert.html', 
							champions=champions)

#Cool idea, just decided to link our lists to the LoL Wiki page however.
# @app.route('/Champion/<string:champ_name>')
# def champ(champ_name):
# 	champions = list_view[champ_name]
# 	for champion in champions:
# 		return render_template('character.html', champion=champion)

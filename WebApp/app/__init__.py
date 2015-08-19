from flask import Flask, request
from flaskext.couchdb import CouchDBManager
import couchdb

manager = CouchDBManager()
server = couchdb.Server()

app = Flask(__name__)
app.config.from_object('config')

manager.setup(app)

from app import views
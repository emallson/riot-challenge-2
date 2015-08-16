from flask import render_template, flash, redirect, g, request
from app import app
from .forms import LoginForm
from werkzeug.local import LocalProxy
import simplejson
couch = LocalProxy(lambda: g.couch)

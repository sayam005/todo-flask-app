from flask import Blueprint

lists = Blueprint('lists', __name__)

from app.blueprints.lists import routes

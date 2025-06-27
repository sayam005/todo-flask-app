from flask import Blueprint

todos = Blueprint('todos', __name__)

from app.blueprints.todos import routes

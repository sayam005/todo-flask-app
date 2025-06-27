from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    
    # Register blueprints
    from app.blueprints.main.routes import main
    from app.blueprints.auth.routes import auth
    from app.blueprints.todos.routes import todos
    from app.blueprints.lists.routes import lists
    
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(todos, url_prefix='/todos')
    app.register_blueprint(lists, url_prefix='/lists')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

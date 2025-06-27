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
    from app.blueprints.achievements import create_achievements_blueprint
    
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(todos, url_prefix='/todos')
    app.register_blueprint(lists, url_prefix='/lists')
    app.register_blueprint(create_achievements_blueprint())
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Initialize achievements on first run
        try:
            from app.blueprints.achievements.services import AchievementService
            AchievementService.initialize_achievements()
        except Exception as e:
            pass  # Ignore if already initialized or other errors
    
    # Context processor to make current_user available in templates
    @app.context_processor
    def inject_user():
        from flask import session
        from app.models import User
        current_user = None
        if 'user_id' in session:
            current_user = User.query.get(session['user_id'])
        return dict(current_user=current_user)
    
    return app

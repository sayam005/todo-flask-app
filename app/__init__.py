from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todiy_fresh.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    
    # Import models to register them
    from app.models import User, Todo, TaskList
    
    # Register basic blueprints first
    from app.blueprints.main.routes import main
    from app.blueprints.auth.routes import auth
    from app.blueprints.todos.routes import todos
    from app.blueprints.lists.routes import lists
    
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(todos, url_prefix='/todos')
    app.register_blueprint(lists, url_prefix='/lists')
    
    # Context processor to make current_user and user stats available in templates
    @app.context_processor
    def inject_user():
        from flask import session
        from app.models import User
        from app.utils import get_user_stats
        
        current_user = None
        user_stats = None
        
        if 'user_id' in session:
            current_user = User.query.get(session['user_id'])
            if current_user:
                user_stats = get_user_stats(session['user_id'])
                
        return dict(current_user=current_user, user_stats=user_stats)
    
    return app

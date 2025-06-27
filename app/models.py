from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    # Add relationships
    todos = db.relationship('Todo', backref='author', lazy=True)
    task_lists = db.relationship('TaskList', backref='owner', lazy=True)
    achievements = db.relationship('UserAchievement', backref='user', lazy=True)
    
    def get_or_create_stats(self):
        """Get user stats, create if doesn't exist"""
        from app.blueprints.achievements.models import UserStats
        if not hasattr(self, 'stats') or not self.stats:
            stats = UserStats.query.filter_by(user_id=self.id).first()
            if not stats:
                stats = UserStats(user_id=self.id)
                db.session.add(stats)
                db.session.commit()
            return stats
        return self.stats
    
    def __repr__(self):
        return f"User('{self.username}')"

class TaskList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    color = db.Column(db.String(7), default='#2196F3', nullable=False)
    emoji = db.Column(db.String(10), default='📋', nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    # Relationship to todos
    todos = db.relationship('Todo', backref='task_list', lazy=True)
    
    def __repr__(self):
        return f"TaskList('{self.name}', '{self.emoji}')"

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    category = db.Column(db.String(20), default='daily', nullable=False)
    custom_deadline = db.Column(db.DateTime, nullable=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # NEW: List assignment and scheduling
    list_id = db.Column(db.Integer, db.ForeignKey('task_list.id'), nullable=True)
    scheduled_date = db.Column(db.Date, nullable=True)
    
    def __repr__(self):
        return f"Todo('{self.title}', '{self.date_created}')"

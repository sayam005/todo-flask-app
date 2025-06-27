from app import db
from datetime import datetime, date, timedelta

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    emoji = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(20), nullable=False)  # 'task', 'streak', 'list'
    requirement = db.Column(db.Integer, nullable=False)  # Number needed to unlock
    
class UserAchievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    achievement = db.relationship('Achievement', backref='user_achievements')

class UserStats(db.Model):
    """Separate stats table to keep User model clean"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    
    # Task stats
    total_completed_tasks = db.Column(db.Integer, default=0)
    total_created_tasks = db.Column(db.Integer, default=0)
    total_lists_created = db.Column(db.Integer, default=0)
    
    # Streak stats
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_activity_date = db.Column(db.Date, default=date.today)
    
    # Rank system
    current_rank = db.Column(db.String(30), default='Iron I')
    rank_points = db.Column(db.Integer, default=0)
    
    # Relationship back to user
    user = db.relationship('User', backref=db.backref('stats', uselist=False))

from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app.blueprints.achievements.models import Achievement, UserAchievement
from app.blueprints.achievements.services import AchievementService, RankService, StreakService

achievements = Blueprint('achievements', __name__, url_prefix='/achievements')

def is_logged_in():
    return 'user_id' in session

@achievements.route('/')
def view_achievements():
    if not is_logged_in():
        flash('Please log in first.', 'danger')
        return redirect(url_for('auth.login'))
    
    from app.models import User
    user = User.query.get(session['user_id'])
    stats = user.get_or_create_stats()
    
    # Get all achievements
    all_achievements = Achievement.query.order_by(Achievement.category, Achievement.requirement).all()
    earned_achievements = [ua.achievement for ua in user.achievements]
    earned_ids = [a.id for a in earned_achievements]
    
    # Group achievements by category
    achievements_by_category = {}
    for achievement in all_achievements:
        if achievement.category not in achievements_by_category:
            achievements_by_category[achievement.category] = {'earned': [], 'locked': []}
        
        if achievement.id in earned_ids:
            achievements_by_category[achievement.category]['earned'].append(achievement)
        else:
            achievements_by_category[achievement.category]['locked'].append(achievement)
    
    # Get rank info
    rank_info = RankService.get_rank_info(stats.rank_points)
    
    # Get streak status
    streak_status = StreakService.get_streak_status(stats)
    
    return render_template('achievements/view.html', 
                         achievements_by_category=achievements_by_category,
                         stats=stats,
                         rank_info=rank_info,
                         streak_status=streak_status,
                         total_earned=len(earned_achievements),
                         total_available=len(all_achievements))

@achievements.route('/initialize')
def initialize():
    """Initialize all achievements (admin route)"""
    if not is_logged_in():
        flash('Please log in first.', 'danger')
        return redirect(url_for('auth.login'))
    
    AchievementService.initialize_achievements()
    flash('🎉 Achievement system initialized!', 'success')
    return redirect(url_for('achievements.view_achievements'))

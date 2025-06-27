from app import db
from app.blueprints.achievements.models import Achievement, UserAchievement, UserStats
from datetime import date, timedelta

class AchievementService:
    @staticmethod
    def initialize_achievements():
        """Create all achievements in database"""
        achievements = [
            # Task Achievements
            {'name': 'First Steps', 'description': 'Complete your first task', 'emoji': '🌱', 'category': 'task', 'requirement': 1},
            {'name': 'Getting Started', 'description': 'Complete 5 tasks', 'emoji': '🚀', 'category': 'task', 'requirement': 5},
            {'name': 'Task Warrior', 'description': 'Complete 10 tasks', 'emoji': '⚔️', 'category': 'task', 'requirement': 10},
            {'name': 'Productivity Master', 'description': 'Complete 25 tasks', 'emoji': '🏆', 'category': 'task', 'requirement': 25},
            {'name': 'Task Legend', 'description': 'Complete 50 tasks', 'emoji': '👑', 'category': 'task', 'requirement': 50},
            {'name': 'Ultimate Achiever', 'description': 'Complete 100 tasks', 'emoji': '💎', 'category': 'task', 'requirement': 100},
            {'name': 'Task Master', 'description': 'Complete 200 tasks', 'emoji': '🏅', 'category': 'task', 'requirement': 200},
            {'name': 'Productivity God', 'description': 'Complete 500 tasks', 'emoji': '⭐', 'category': 'task', 'requirement': 500},
            
            # Streak Achievements
            {'name': 'Daily Habit', 'description': 'Complete tasks for 3 days in a row', 'emoji': '🔥', 'category': 'streak', 'requirement': 3},
            {'name': 'Week Warrior', 'description': 'Complete tasks for 7 days in a row', 'emoji': '📅', 'category': 'streak', 'requirement': 7},
            {'name': 'Consistency King', 'description': 'Complete tasks for 14 days in a row', 'emoji': '👑', 'category': 'streak', 'requirement': 14},
            {'name': 'Month Master', 'description': 'Complete tasks for 30 days in a row', 'emoji': '🗓️', 'category': 'streak', 'requirement': 30},
            {'name': 'Streak Legend', 'description': 'Complete tasks for 50 days in a row', 'emoji': '🔥', 'category': 'streak', 'requirement': 50},
            {'name': 'Unstoppable', 'description': 'Complete tasks for 100 days in a row', 'emoji': '💪', 'category': 'streak', 'requirement': 100},
            
            # List Achievements  
            {'name': 'Organizer', 'description': 'Create your first list', 'emoji': '📋', 'category': 'list', 'requirement': 1},
            {'name': 'List Master', 'description': 'Create 5 lists', 'emoji': '📂', 'category': 'list', 'requirement': 5},
            {'name': 'Organization Expert', 'description': 'Create 10 lists', 'emoji': '🗂️', 'category': 'list', 'requirement': 10},
        ]
        
        for ach_data in achievements:
            existing = Achievement.query.filter_by(name=ach_data['name']).first()
            if not existing:
                achievement = Achievement(**ach_data)
                db.session.add(achievement)
        
        db.session.commit()
    
    @staticmethod
    def check_and_award_achievements(user_id, category=None):
        """Check if user earned any new achievements"""
        from app.models import User
        user = User.query.get(user_id)
        stats = user.get_or_create_stats()
        
        # Get achievements user doesn't have yet
        earned_achievement_ids = [ua.achievement_id for ua in user.achievements]
        
        if category:
            available_achievements = Achievement.query.filter(
                Achievement.category == category,
                ~Achievement.id.in_(earned_achievement_ids)
            ).all()
        else:
            available_achievements = Achievement.query.filter(
                ~Achievement.id.in_(earned_achievement_ids)
            ).all()
        
        new_achievements = []
        
        for achievement in available_achievements:
            earned = False
            
            if achievement.category == 'task':
                earned = stats.total_completed_tasks >= achievement.requirement
            elif achievement.category == 'streak':
                earned = stats.current_streak >= achievement.requirement
            elif achievement.category == 'list':
                earned = stats.total_lists_created >= achievement.requirement
            
            if earned:
                # Award achievement
                user_achievement = UserAchievement(
                    user_id=user_id,
                    achievement_id=achievement.id
                )
                db.session.add(user_achievement)
                new_achievements.append(achievement)
        
        if new_achievements:
            db.session.commit()
        
        return new_achievements

class RankService:
    @staticmethod
    def get_rank_info(rank_points):
        """Get rank info based on points (like Valorant)"""
        ranks = [
            {'name': 'Iron I', 'min_points': 0, 'emoji': '⚫', 'color': '#4A4A4A'},
            {'name': 'Iron II', 'min_points': 50, 'emoji': '⚫', 'color': '#4A4A4A'},
            {'name': 'Iron III', 'min_points': 100, 'emoji': '⚫', 'color': '#4A4A4A'},
            {'name': 'Bronze I', 'min_points': 200, 'emoji': '🥉', 'color': '#CD7F32'},
            {'name': 'Bronze II', 'min_points': 300, 'emoji': '🥉', 'color': '#CD7F32'},
            {'name': 'Bronze III', 'min_points': 450, 'emoji': '🥉', 'color': '#CD7F32'},
            {'name': 'Silver I', 'min_points': 600, 'emoji': '🥈', 'color': '#C0C0C0'},
            {'name': 'Silver II', 'min_points': 800, 'emoji': '🥈', 'color': '#C0C0C0'},
            {'name': 'Silver III', 'min_points': 1000, 'emoji': '🥈', 'color': '#C0C0C0'},
            {'name': 'Gold I', 'min_points': 1300, 'emoji': '🥇', 'color': '#FFD700'},
            {'name': 'Gold II', 'min_points': 1600, 'emoji': '🥇', 'color': '#FFD700'},
            {'name': 'Gold III', 'min_points': 2000, 'emoji': '🥇', 'color': '#FFD700'},
            {'name': 'Platinum I', 'min_points': 2500, 'emoji': '💎', 'color': '#E5E4E2'},
            {'name': 'Platinum II', 'min_points': 3000, 'emoji': '💎', 'color': '#E5E4E2'},
            {'name': 'Platinum III', 'min_points': 3600, 'emoji': '💎', 'color': '#E5E4E2'},
            {'name': 'Diamond I', 'min_points': 4300, 'emoji': '💠', 'color': '#B9F2FF'},
            {'name': 'Diamond II', 'min_points': 5000, 'emoji': '💠', 'color': '#B9F2FF'},
            {'name': 'Diamond III', 'min_points': 6000, 'emoji': '💠', 'color': '#B9F2FF'},
            {'name': 'Immortal I', 'min_points': 7500, 'emoji': '🔮', 'color': '#FF6B6B'},
            {'name': 'Immortal II', 'min_points': 9000, 'emoji': '🔮', 'color': '#FF6B6B'},
            {'name': 'Immortal III', 'min_points': 11000, 'emoji': '🔮', 'color': '#FF6B6B'},
            {'name': 'Radiant', 'min_points': 15000, 'emoji': '🌟', 'color': '#FF1493'},
        ]
        
        current_rank = ranks[0]
        for rank in ranks:
            if rank_points >= rank['min_points']:
                current_rank = rank
        
        # Find next rank
        next_rank = None
        for rank in ranks:
            if rank['min_points'] > rank_points:
                next_rank = rank
                break
        
        # Calculate progress
        progress = 0
        if next_rank:
            current_min = current_rank['min_points']
            next_min = next_rank['min_points']
            progress = ((rank_points - current_min) / (next_min - current_min)) * 100
            progress = min(100, max(0, progress))
        else:
            progress = 100  # Max rank achieved
        
        return {'current': current_rank, 'next': next_rank, 'progress': progress}

class StreakService:
    @staticmethod
    def update_streak(user_stats, completed_task_today=True):
        """Update streak system like Duolingo"""
        today = date.today()
        
        if completed_task_today:
            if user_stats.last_activity_date == today:
                # Already completed task today, no streak change
                return False, "Same day completion"
            elif user_stats.last_activity_date == today - timedelta(days=1):
                # Completed task yesterday, continue streak
                user_stats.current_streak += 1
                user_stats.last_activity_date = today
                if user_stats.current_streak > user_stats.longest_streak:
                    user_stats.longest_streak = user_stats.current_streak
                return True, f"Streak continued! {user_stats.current_streak} days"
            else:
                # Broke streak, restart
                old_streak = user_stats.current_streak
                user_stats.current_streak = 1
                user_stats.last_activity_date = today
                return True, f"Streak restarted! Was {old_streak}, now 1 day"
        
        return False, "No update"
    
    @staticmethod
    def get_streak_status(user_stats):
        """Get streak status and motivation message"""
        today = date.today()
        
        if user_stats.last_activity_date == today:
            return {
                'status': 'active',
                'message': f"🔥 {user_stats.current_streak} day streak! Keep it up!",
                'color': '#FF6B35'
            }
        elif user_stats.last_activity_date == today - timedelta(days=1):
            return {
                'status': 'at_risk',
                'message': f"⚠️ {user_stats.current_streak} day streak at risk! Complete a task today!",
                'color': '#FFA500'
            }
        else:
            return {
                'status': 'broken',
                'message': "💔 Streak broken. Start a new one today!",
                'color': '#DC3545'
            }

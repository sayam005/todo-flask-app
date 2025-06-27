#!/usr/bin/env python3
"""
Simple test script to check if the toDIY app works properly
"""

from app import create_app, db
from app.models import User, TaskList, Todo
from app.blueprints.achievements.models import Achievement, UserStats, UserAchievement
from app.blueprints.achievements.services import AchievementService, RankService, StreakService

def test_app():
    print("🧪 Testing toDIY App...")
    
    app = create_app()
    with app.app_context():
        print("✅ App created successfully!")
        
        # Test database tables
        try:
            # Check if tables exist
            users = User.query.all()
            achievements = Achievement.query.all()
            print(f"✅ Database working! Found {len(users)} users and {len(achievements)} achievements")
        except Exception as e:
            print(f"❌ Database error: {e}")
            return False
        
        # Test achievement initialization
        try:
            AchievementService.initialize_achievements()
            achievements = Achievement.query.all()
            print(f"✅ Achievements initialized! Total: {len(achievements)}")
            
            # Show some achievements
            for ach in achievements[:3]:
                print(f"   {ach.emoji} {ach.name}: {ach.description}")
                
        except Exception as e:
            print(f"❌ Achievement initialization error: {e}")
            return False
        
        # Test rank system
        try:
            rank_info = RankService.get_rank_info(0)
            print(f"✅ Rank system working! Starting rank: {rank_info['current']['emoji']} {rank_info['current']['name']}")
            
            rank_info = RankService.get_rank_info(500)
            print(f"   At 500 points: {rank_info['current']['emoji']} {rank_info['current']['name']}")
            
        except Exception as e:
            print(f"❌ Rank system error: {e}")
            return False
        
        print("\n🎉 All tests passed! Your toDIY app is ready to use!")
        print("\n🚀 To start the app, run: python app.py")
        print("📝 Then go to: http://localhost:5000")
        
        return True

if __name__ == "__main__":
    test_app()

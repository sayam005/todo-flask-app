from app import create_app
from app import db

app = create_app()

with app.app_context():
    db.create_all()
    from app.blueprints.achievements.services import AchievementService
    AchievementService.initialize_achievements()

if __name__ == '__main__':
    app.run(debug=True)

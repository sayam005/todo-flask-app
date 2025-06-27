from flask import Blueprint

def create_achievements_blueprint():
    from app.blueprints.achievements.routes import achievements
    return achievements

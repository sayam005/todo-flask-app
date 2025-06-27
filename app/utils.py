from app.models import Todo, TaskList, User

def get_user_rank(completed_tasks_count):
    """
    Calculate user rank based on completed tasks count.
    Simple progression system inspired by gaming platforms.
    """
    if completed_tasks_count == 0:
        return "Unranked", "🥅"
    elif completed_tasks_count < 5:
        return "Beginner", "🌱"
    elif completed_tasks_count < 15:
        return "Worker", "⚡"
    elif completed_tasks_count < 30:
        return "Expert", "🔥"
    else:
        return "Master", "👑"

def get_user_stats(user_id):
    """
    Get comprehensive user statistics for display.
    Returns a dictionary with user stats and rank info.
    """
    # Count completed tasks
    completed_tasks = Todo.query.filter_by(user_id=user_id, completed=True).count()
    
    # Count total tasks
    total_tasks = Todo.query.filter_by(user_id=user_id).count()
    
    # Count user's lists
    total_lists = TaskList.query.filter_by(user_id=user_id).count()
    
    # Get rank
    rank_name, rank_emoji = get_user_rank(completed_tasks)
    
    return {
        'completed_tasks': completed_tasks,
        'total_tasks': total_tasks,
        'total_lists': total_lists,
        'rank_name': rank_name,
        'rank_emoji': rank_emoji,
        'completion_rate': round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1)
    }
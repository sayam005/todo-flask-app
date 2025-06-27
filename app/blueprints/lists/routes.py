from flask import Blueprint, render_template, redirect, url_for, flash, session
from app import db
from app.models import TaskList, Todo
from app.blueprints.lists.forms import CreateListForm
from datetime import datetime, timedelta
import random

lists = Blueprint('lists', __name__)

def is_logged_in():
    return 'user_id' in session

def get_random_quote():
    quotes = [
        "Small steps every day lead to big changes one year from now.",
        "Progress, not perfection.",
        "You don't have to be great to get started, but you have to get started to be great.",
        "Focus on being productive instead of busy.",
        "The best time to plant a tree was 20 years ago. The second best time is now.",
        "Don't wait for opportunity. Create it.",
        "Success is the sum of small efforts repeated day in and day out.",
        "What you do today can improve all your tomorrows.",
        "Organize your tasks by topic to stay focused! 🎯"
    ]
    return random.choice(quotes)

@lists.route('/')
def view_lists():
    if not is_logged_in():
        flash('Please log in first.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get user's lists with task counts
    user_lists = TaskList.query.filter_by(user_id=session['user_id']).all()
    
    # Add task counts to each list
    for task_list in user_lists:
        task_list.total_tasks = len(task_list.todos)
        task_list.completed_tasks = len([todo for todo in task_list.todos if todo.completed])
        task_list.pending_tasks = task_list.total_tasks - task_list.completed_tasks
    
    return render_template('lists/view_lists.html', 
                         lists=user_lists, 
                         username=session['username'],
                         quote=get_random_quote())

@lists.route('/create', methods=['GET', 'POST'])
def create_list():
    if not is_logged_in():
        flash('Please log in first.', 'danger')
        return redirect(url_for('auth.login'))
    
    form = CreateListForm()
    if form.validate_on_submit():
        # Check if list name already exists for this user
        existing_list = TaskList.query.filter_by(
            name=form.name.data, 
            user_id=session['user_id']
        ).first()
        
        if existing_list:
            flash('A list with this name already exists!', 'danger')
            return render_template('lists/create_list.html', form=form)
        
        task_list = TaskList(
            name=form.name.data,
            description=form.description.data,
            emoji=form.emoji.data,
            color=form.color.data,
            user_id=session['user_id']
        )
        db.session.add(task_list)
        db.session.commit()
        
        flash(f'List "{form.emoji.data} {form.name.data}" created successfully!', 'success')
        return redirect(url_for('lists.view_lists'))
    
    return render_template('lists/create_list.html', form=form)

@lists.route('/<int:list_id>')
def view_list_tasks(list_id):
    if not is_logged_in():
        flash('Please log in first.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get the list and make sure user owns it
    task_list = TaskList.query.get_or_404(list_id)
    if task_list.user_id != session['user_id']:
        flash('You can only view your own lists.', 'danger')
        return redirect(url_for('lists.view_lists'))
    
    # Get tasks in this list
    todos = Todo.query.filter_by(list_id=list_id).all()
    
    # Add time calculations for each task
    for todo in todos:
        now = datetime.now()
        created_date = todo.date_created
        
        if todo.category == 'custom' and todo.custom_deadline:
            deadline = todo.custom_deadline
        elif todo.category == 'daily':
            deadline = created_date.replace(hour=23, minute=59, second=59)
            if now.date() > created_date.date():
                deadline = now.replace(hour=23, minute=59, second=59)
        elif todo.category == 'weekly':
            deadline = created_date + timedelta(days=7)
        elif todo.category == 'monthly':
            deadline = created_date + timedelta(days=30)
        else:
            deadline = created_date.replace(hour=23, minute=59, second=59)
        
        time_remaining = deadline - now
        todo.deadline = deadline
        todo.time_remaining = time_remaining
        todo.is_overdue = time_remaining.total_seconds() < 0 and not todo.completed
        
        if time_remaining.total_seconds() < 0:
            todo.time_display = "Overdue!"
        elif time_remaining.days > 0:
            hours = time_remaining.seconds // 3600
            todo.time_display = f"{time_remaining.days}d {hours}h remaining"
        else:
            hours = time_remaining.seconds // 3600
            minutes = (time_remaining.seconds % 3600) // 60
            todo.time_display = f"{hours}h {minutes}m remaining"
    
    return render_template('lists/list_tasks.html', 
                         task_list=task_list, 
                         todos=todos, 
                         username=session['username'])

@lists.route('/delete/<int:list_id>')
def delete_list(list_id):
    if not is_logged_in():
        flash('Please log in first.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get the list and make sure user owns it
    task_list = TaskList.query.get_or_404(list_id)
    if task_list.user_id != session['user_id']:
        flash('You can only delete your own lists.', 'danger')
        return redirect(url_for('lists.view_lists'))
    
    # Store list name for flash message
    list_name = f"{task_list.emoji} {task_list.name}"
    
    # Delete the list (this will also delete all associated todos due to cascade)
    db.session.delete(task_list)
    db.session.commit()
    
    flash(f'List "{list_name}" and all its tasks have been deleted successfully!', 'success')
    return redirect(url_for('lists.view_lists'))

@lists.route('/schedule')
def daily_schedule():
    if not is_logged_in():
        flash('Please log in first.', 'danger')
        return redirect(url_for('auth.login'))
    
    today = datetime.now().date()
    
    # Get tasks scheduled for today from ALL lists
    todays_tasks = Todo.query.filter_by(
        user_id=session['user_id'],
        scheduled_date=today
    ).all()
    
    # Group tasks by list
    tasks_by_list = {}
    unassigned_tasks = []
    
    for todo in todays_tasks:
        # Add time calculations
        now = datetime.now()
        created_date = todo.date_created
        
        if todo.category == 'custom' and todo.custom_deadline:
            deadline = todo.custom_deadline
        elif todo.category == 'daily':
            deadline = created_date.replace(hour=23, minute=59, second=59)
            if now.date() > created_date.date():
                deadline = now.replace(hour=23, minute=59, second=59)
        elif todo.category == 'weekly':
            deadline = created_date + timedelta(days=7)
        elif todo.category == 'monthly':
            deadline = created_date + timedelta(days=30)
        else:
            deadline = created_date.replace(hour=23, minute=59, second=59)
        
        time_remaining = deadline - now
        todo.deadline = deadline
        todo.time_remaining = time_remaining
        todo.is_overdue = time_remaining.total_seconds() < 0 and not todo.completed
        
        if time_remaining.total_seconds() < 0:
            todo.time_display = "Overdue!"
        elif time_remaining.days > 0:
            hours = time_remaining.seconds // 3600
            todo.time_display = f"{time_remaining.days}d {hours}h remaining"
        else:
            hours = time_remaining.seconds // 3600
            minutes = (time_remaining.seconds % 3600) // 60
            todo.time_display = f"{hours}h {minutes}m remaining"
        
        # Group by list
        if todo.task_list:
            list_key = f"{todo.task_list.emoji} {todo.task_list.name}"
            if list_key not in tasks_by_list:
                tasks_by_list[list_key] = {
                    'tasks': [],
                    'color': todo.task_list.color,
                    'list_obj': todo.task_list
                }
            tasks_by_list[list_key]['tasks'].append(todo)
        else:
            unassigned_tasks.append(todo)
    
    return render_template('lists/daily_schedule.html', 
                         tasks_by_list=tasks_by_list, 
                         unassigned_tasks=unassigned_tasks,
                         today=today,
                         username=session['username'],
                         quote=get_random_quote())

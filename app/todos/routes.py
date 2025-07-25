from flask import Blueprint, render_template, redirect, url_for, flash, session
from datetime import datetime, timedelta
from app import db
from app.models import Todo
from app.todos.forms import TodoForm

todos = Blueprint('todos', __name__)

# Helper function to check if user is logged in
def is_logged_in():
    return 'user_id' in session

@todos.route('/dashboard')
def dashboard():
    if not is_logged_in():
        flash('Please log in to access your dashboard.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get current user's todos
    todos_list = Todo.query.filter_by(user_id=session['user_id']).all()
    
    # Add time-related info to each todo
    for todo in todos_list:
        # Calculate time remaining based on category
        now = datetime.now()
        created_date = todo.date_created
        
        if todo.category == 'daily':
            # Daily tasks expire at end of day they were created
            deadline = created_date.replace(hour=23, minute=59, second=59)
            if now.date() > created_date.date():
                deadline = now.replace(hour=23, minute=59, second=59)  # Today's end
        elif todo.category == 'weekly':
            # Weekly tasks expire after 7 days
            deadline = created_date + timedelta(days=7)
        elif todo.category == 'monthly':
            # Monthly tasks expire after 30 days
            deadline = created_date + timedelta(days=30)
        else:
            # Default: daily
            deadline = created_date.replace(hour=23, minute=59, second=59)
        
        # Calculate time remaining
        time_remaining = deadline - now
        
        # Add attributes to todo object
        todo.deadline = deadline
        todo.time_remaining = time_remaining
        todo.is_overdue = time_remaining.total_seconds() < 0 and not todo.completed
        
        # Calculate urgency (less than 25% of time remaining for incomplete tasks)
        total_time = deadline - created_date
        if not todo.completed and not todo.is_overdue:
            time_used = now - created_date
            todo.is_urgent = time_used > total_time * 0.75  # More than 75% time used
        else:
            todo.is_urgent = False
        
        # Format time remaining for display
        if time_remaining.total_seconds() < 0:
            todo.time_display = "Overdue!"
        elif time_remaining.days > 0:
            hours = time_remaining.seconds // 3600
            todo.time_display = f"{time_remaining.days}d {hours}h remaining"
        else:
            hours = time_remaining.seconds // 3600
            minutes = (time_remaining.seconds % 3600) // 60
            todo.time_display = f"{hours}h {minutes}m remaining"
    
    return render_template('todos/dashboard.html', todos=todos_list, username=session['username'])

@todos.route('/add', methods=['GET', 'POST'])
def add_todo():
    if not is_logged_in():
        flash('Please log in first.', 'danger')
        return redirect(url_for('auth.login'))
    
    form = TodoForm()
    if form.validate_on_submit():
        todo = Todo(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            user_id=session['user_id']
        )
        db.session.add(todo)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('todos.dashboard'))
    
    return render_template('todos/add_todo.html', form=form)

@todos.route('/complete/<int:todo_id>')
def complete_todo(todo_id):
    if not is_logged_in():
        flash('Please log in first.', 'danger')
        return redirect(url_for('auth.login'))
    
    todo = Todo.query.get_or_404(todo_id)
    # Make sure user owns this todo
    if todo.user_id != session['user_id']:
        flash('You can only modify your own tasks.', 'danger')
        return redirect(url_for('todos.dashboard'))
    
    todo.completed = not todo.completed
    db.session.commit()
    flash('Task updated!', 'success')
    return redirect(url_for('todos.dashboard'))

@todos.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    if not is_logged_in():
        flash('Please log in first.', 'danger')
        return redirect(url_for('auth.login'))
    
    todo = Todo.query.get_or_404(todo_id)
    # Make sure user owns this todo
    if todo.user_id != session['user_id']:
        flash('You can only delete your own tasks.', 'danger')
        return redirect(url_for('todos.dashboard'))
    
    db.session.delete(todo)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('todos.dashboard'))

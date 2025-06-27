from flask import Flask

# Create Flask app instance
app = Flask(__name__)

# Basic route for home page
@app.route('/')
def home():
    return '<h1>Welcome to My Todo App!</h1><p>This is your first Flask app!</p>'

# Basic route for testing
@app.route('/test')
def test():
    return '<h2>Test page works</h2>'

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

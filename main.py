from flask_resume import create_app

# Call the Application Factory function to construct a Flask application instance
# using the standard configuration defined in /instance/flask.cfg
app = create_app('dev.cfg')
app.run(debug=True)
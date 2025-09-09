from flask import Flask, jsonify
from database import app, db
from controllers import api
from visualization import viz
import os

# Register Blueprints
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(viz, url_prefix='/api')

# Global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    # Here you can add logging e.g. to a file
    return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create database tables if they don't exist
    if not os.path.exists('budget_planner.db'):
        with app.app_context():
            db.create_all()
    
    app.run()

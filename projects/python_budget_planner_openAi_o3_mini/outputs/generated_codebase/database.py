from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import json

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['database']['uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(port=config['server']['port'], debug=(config['server']['environment'] == 'development'))

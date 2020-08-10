from flask_sqlalchemy import SQLAlchemy
from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:$ssmi119$@localhost:3306/api_2'
#app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

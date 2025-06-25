from flask import Flask
from flask_cors import CORS
from extensions import db
from utils.mail import mail 
from routes.user import user_bp
from routes.attendance import attendance_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
mail.init_app(app) 
CORS(app)

app.register_blueprint(user_bp)
app.register_blueprint(attendance_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

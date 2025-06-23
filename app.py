from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from models import db
import config
from utils.mail_utils import mail

from routes.attendance import attendance_bp

app = Flask(__name__)
app.config.from_object(config)

CORS(app)
db.init_app(app)
mail.init_app(app)

app.register_blueprint(attendance_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

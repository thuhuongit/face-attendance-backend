# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:@localhost/face_attendance"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'hle183414@gmail.com'
    MAIL_PASSWORD = 'dhbcsrwarnimptgu'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

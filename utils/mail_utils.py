from flask_mail import Mail, Message

mail = Mail()

def send_attendance_email(to_email, name, time_str):
    subject = "Xác nhận điểm danh"
    body = f"Chào {name}, bạn đã điểm danh lúc {time_str}. Trân trọng."

    msg = Message(subject,
                  sender="youremail@gmail.com",
                  recipients=[to_email])
    msg.body = body
    mail.send(msg)

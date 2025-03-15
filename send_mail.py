import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from model import Session, User, Location


def send_email_on_new_review(location_id):
    with Session() as session:
        location = session.query(Location).filter_by(id=location_id).first()
        if not location:
            return
        owner = session.query(User).filter_by(id=location.user_id).first()
        if not owner:
            return

        sender_email = "fghttt@ukr.net"
        sender_password = "uJwm6zeXWebJaibW"

        subject = "Новий відгук на вашу локацію!"
        body = f"На вашу локацію '{location.name}' було залишено новий відгук. Перегляньте його у додатку."

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = owner.email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP_SSL("smtp.ukr.net", 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, owner.email, msg.as_string())
        except Exception as exception:
            print(f"Помилка: {exception}")
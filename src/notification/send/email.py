import smtplib, os
from email.message import EmailMessage
import json


def notification(message):
    try:
        message = json.loads(message)
        mp3_fid = message["mp3_fid"]
        sender_add = os.environ.get("GMAIL_ADD")
        sender_pass = os.environ.get("GMAIL_PASS")
        receiver_add = message["username"]

        msg = EmailMessage()
        msg.set_content(f"mp3 file_id: {mp3_fid} is now ready")
        msg["Subject"] = "MP3 Download"
        msg["From"] = sender_add
        msg["To"] = receiver_add

        session = smtplib.SMTP("smtp.gmail.com", 587)
        session.starttls()
        session.login(sender_add, sender_pass)
        session.send_message(msg, sender_add, receiver_add)
        session.quit()
        print("mail sent")

    except Exception as ex:
        print(f"Error sending email: {ex}")
        return None

        


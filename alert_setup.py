from email.message import EmailMessage
import smtplib
from os import environ as env
from dotenv import load_dotenv

load_dotenv()

def email_alert(subject,body,to):
    msg=EmailMessage()
    msg.set_content(body)
    msg['subject']=subject
    msg['to']=to
    user=env['user']
    password=env['password']
    msg['from']=user
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)
    server.quit()
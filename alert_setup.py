import smtplib
from os import environ as env
from dotenv import load_dotenv
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class email_alert:
    load_dotenv()
    def __init__(self):
        self.user=env['user']
        self.password=env['password'] 

    def alert(self,to,df):
        msg=MIMEMultipart()
        # Compose email html body
        body=f"&#10071;&#10071;&#10071;<br><br> We found { len(df) } campsites available.<br>Let's go camping &#127758;&#127758;&#127758;<br>"
        html = """\
        <html>
            <head></head>
                <body>
                    {0}
                    {1}
                </body>
        </html>
        """.format(body, df.to_html(index=False))
        part=MIMEText(html,'html')
        msg.attach(part)
        msg['subject']='Your Campsite Available !!!'
        with smtplib.SMTP("smtp.gmail.com",587) as server:
            server.starttls()
            server.login(self.user,self.password)
            server.sendmail(from_addr=self.user,msg=msg.as_string(),to_addrs=to)
        
    def welcome(self,to):
        msg=MIMEMultipart()
        # Compose email html body
        body="&#9978;&#9978;&#9978;&#9978;<br><br> Welcome! Your favoriate campsites are being monitored. <br><br> You will be emailed if any new availabilities open up! "
        html = """\
        <html>
            <head></head>
                <body>
                    {0}
                </body>
        </html>
        """.format(body)
        part=MIMEText(html,'html')
        msg.attach(part)
        msg['subject']='Camper X Got You! ✨ ✨ ✨ '
        with smtplib.SMTP("smtp.gmail.com",587) as server:
            server.starttls()
            server.login(self.user,self.password)
            server.sendmail(from_addr=self.user,msg=msg.as_string(),to_addrs=to)
        



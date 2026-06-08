import os
from dotenv import load_dotenv
import smtplib

class MailManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        load_dotenv()
        self.gmail_user = os.environ["GMAIL_USER"]
        self.gmail_password = os.environ["GMAIL_PASSWORD"]

    def sendmails(self, email_list, message_body, destination):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=self.gmail_user, password=self.gmail_password)
            for email in email_list:
                connection.sendmail(
                    from_addr=self.gmail_user,
                    to_addrs=email,
                    msg=f"Subject:I found you a cheaper flight to {destination}\n\n{message_body}",
                )
                print(f"mail sent! ({destination}) to {email}")

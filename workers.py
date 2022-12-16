import datetime
import smtplib, ssl
from os import environ
from celery import Celery
from celery.schedules import crontab
from flask import current_app as app
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from models import user_datastore, KanbanList, KanbanCard

celery = Celery("Application Jobs")

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executes every day at 8:00 a.m.
    sender.add_periodic_task(
        crontab(hour=8, minute=0),
        send_daily_email.s(),
    )

    # Executes every month on the 1st at 8:00 a.m.
    sender.add_periodic_task(
        crontab(day_of_month=1, hour=8, minute=0),
        send_monthly_email.s(),
    )


port = 465
smtp_server = "smtp.gmail.com"
sender_email = "21f1002218@student.onlinedegree.iitm.ac.in"
password = environ.get('EMAIL_PASSWORD')

@celery.task
def send_daily_email():   
    for user in user_datastore.find_all_users():
        receiver_email = user.email

        cards: list[KanbanCard] = KanbanCard.query.filter_by(user_id=user.id).all()

        # Find cards that are due today
        today_cards = []
        for card in cards:
            if card.completed==False and card.deadline <= datetime.datetime.today():
                today_cards.append(card.title)
        
        # Send email if there are cards due today
        message = f"""
            Subject: Kanban Cards Due Today

            You have the following cards due today:
            <ul>
                { [card for card in today_cards] }
            </ul>
        """

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

@celery.task
def send_monthly_email():
    for user in user_datastore.find_all_users():
        receiver_email = user.email

        lists: list[KanbanList] = KanbanList.query.filter_by(user_id=user.id).all()
        cards = KanbanCard.query.filter_by(user_id=user.id).all()

        message = MIMEMultipart("alternative")
        message["Subject"] = "Monthly Kanban Report"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = """
            Hi { user.email.split('@')[0] },
            This is a monthly report of your Kanban cards.
        """

        html = f"""
            <html>
                <body>
                    <h2> Kanban Report </h2>
                    <h3> Month { datetime.datetime.today().month}</h3>
                    <p>
                        You have { len(lists) } active lists.
                        <br/>
                        You have { len(cards) } active cards.
                        <br/>
                        You have the following cards due this month:
                        <ul>
                            { [card.title for card in cards if card.completed==False and card.deadline.month == datetime.datetime.today().month] }
                        </ul>
                        <br/>
                        Make sure to complete them! <br/>
                        Your favourite Kanban app.
                    </p>
                </body>
            </html>
        """

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
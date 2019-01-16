from flask_mail import Message
from flask import render_template
from app import app, mail
from threading import Thread

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
	"""
	subject: str, subject line
	sender: str, email ID of sender
	recipients: list, email ID(s) of recipients
	text_body: str, contents of the email body
	html_body: str, contents of the email in HTML format
	"""
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html_body = html_body
	Thread(target = send_async_email, args = (app, msg)).start()


def send_password_reset_email(user):
	token = user.reset_password_token()
	subject = '[Microblog] Reset Your Password'
	sender = app.config['ADMINS'][0]
	recipients = [user.email]
	text_body=render_template('email/reset_password.txt', user=user, token=token)
	html_body=render_template('email/reset_password.html', user=user, token=token)
	send_email(subject, sender, recipients, text_body, html_body)





from flask_mail import Mail,Message
import consts
from . import mail, celery
from threading import Thread
from flask import current_app, render_template

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def send_email_by_thread(recipient,subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject = subject, sender= app.config['FLASKY_MAIL_SENDER'], recipients= [recipient])
    msg.body = render_template(template+'.txt', **kwargs)
    msg.html = render_template(template+'.html', **kwargs)
    thr = Thread(target= send_async_email, args=[app,msg])
    thr.start()
    return thr

@celery.task
def send_async_email_by_celery(recipient,subject, template, **kwargs):
    app = current_app._get_current_object()
    with app.app_context():
        msg = Message(subject=subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[recipient])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        mail.send(msg)
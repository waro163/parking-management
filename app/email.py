from flask_mail import Mail,Message
import consts
from . import mail
from threading import Thread
from flask import current_app, render_template

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

# def send_email(username,userpasswd):
#     msg=Message('test',recipients=[consts.MAIL_RECEIVEADD],sender=consts.MAIL_USERNAME)
#     # msg.body = 'test body: username %s, password %s' % (username,userpasswd)
#     msg.body = 'test body: username : {username}, password : {password}'.format(username=username,password=userpasswd)
#     mail.send(msg)
#     print ('email send successful!')
#     return

def send_email(recipient,subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject = subject, sender= app.config['FLASKY_MAIL_SENDER'], recipients= recipient)
    msg.body = render_template(template+'.txt', **kwargs)
    msg.html = render_template(template+'.html', **kwargs)
    thr = Thread(target= send_async_email, args=[app,msg])
    thr.start()
    return thr

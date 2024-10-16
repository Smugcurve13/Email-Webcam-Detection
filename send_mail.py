import smtplib
import imghdr
from email.message import EmailMessage

SENDER = ''
PASSWORD = ''
RECEIVER = ''


def send_email(img_path):
    print('send email function started')
    email_msg = EmailMessage
    email_msg['Subject'] = "New Object Detected"
    email_msg.set_content('New Object detected in webcame frame')

    with open(img_path, 'rb') as file:
        content = file.read()
    email_msg.add_attachment(content, maintype='image', subtype=imghdr.what(None, content))
    
    gmail = smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER,PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_msg.as_string())
    gmail.quit()
    print('send email function stopped')

if __name__ == '__main__':
    send_email(img_path='images/test.png')
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import common
from bottle import get

def send_mail(to_address, subject, plain_text_content = None, html_content = None):
    content = ""
    if plain_text_content:
        content = plain_text_content
    elif html_content:
        content = html_content

    message = Mail(
        from_email='twixxer@pinkbananastudio.dk',
        to_emails=to_address,
        subject=subject,
        html_content=content)
    try:
        sg = SendGridAPIClient(common.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

@get(f"/api/email/signup")
def send_signup_email():
    html_email = """\
    <html>
        <body>
        <p>
            Welcome to Twixxer!<br>
            <b style="color: blue;">Keep it Twixxin! Or else get Twixxed.</b><br>
        </p>
        </body>
    </html>
    """
    send_mail("nagy.andor89@gmail.com", "Welcome to Twixxer!", html_content=html_email)

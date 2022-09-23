import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()
EMAILPASS = os.getenv("EMAILPASS")
GMAILKEY = os.getenv("GMAILKEY")


def confirmationEmailSend():

    senderEmail = "cravecravero@gmail.com"
    recieverEmail = "felipecravero05@gmail.com"
    subject = "Email de confirmacion"
    message = "hola, confirme su correo electronico"

    em = EmailMessage()
    em["From"] = senderEmail
    em["To"] = recieverEmail
    em["Subject"] = subject
    em.set_content(message)

    with smtplib.SMTP_SSL(host="smtp.gmail.com", port=587) as smtp:
        smtp.starttls()
        smtp.login(user=senderEmail, password=GMAILKEY)
        smtp.sendmail(
            from_addr=senderEmail, to_addrs=recieverEmail, msg="em.as_string()"
        )


confirmationEmailSend()
print("hola")

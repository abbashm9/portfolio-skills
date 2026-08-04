import base64
import json
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

with open("outbox/email.json") as f:
    raw = f.read()

# The routine agent sometimes base64-encodes the JSON itself before the GitHub
# connector encodes it again, leaving base64 text in the file (2026-08-02 miss).
try:
    data = json.loads(raw)
except json.JSONDecodeError:
    data = json.loads(base64.b64decode(raw))

subject = data.get("subject", "Daily Portfolio Check")
html_body = data.get("html_body", "")

if not html_body:
    print("outbox/email.json has no html_body — skipping send.")
    exit(0)

msg = MIMEMultipart("alternative")
msg["Subject"] = subject
msg["From"] = "almadani.abbas@gmail.com"
msg["To"] = "almadani.abbas@gmail.com"
msg.attach(MIMEText(html_body, "html"))

password = os.environ["GMAIL_APP_PASSWORD"]

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login("almadani.abbas@gmail.com", password)
    server.sendmail("almadani.abbas@gmail.com", "almadani.abbas@gmail.com", msg.as_string())

print(f"Email sent: {subject}")

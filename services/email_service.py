import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path


def send_processed_images(file_paths: dict) -> None:
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_APP_PASSWORD")
    recipient_email = os.environ.get("RECIPIENT_EMAIL")
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))

    if not sender_email or not sender_password or not recipient_email:
        raise EnvironmentError(
            "Missing required environment variables: SENDER_EMAIL, SENDER_APP_PASSWORD, RECIPIENT_EMAIL"
        )

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = "Processed Logo Output Results"

    body = (
        "Please find attached the 3 processed versions of your uploaded logo:\n\n"
        "  - silhouette.png : Solid filled shape with no internal details\n"
        "  - border.png     : Outline/edge-only version\n"
        "  - grayscale.png  : Standard grayscale version\n\n"
        "These images were generated automatically by the Logo Processing Service."
    )
    msg.attach(MIMEText(body, "plain"))

    for label, path_str in file_paths.items():
        path = Path(path_str)
        if not path.exists():
            raise FileNotFoundError(f"Attachment not found: {path_str}")

        with open(path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={path.name}",
        )
        msg.attach(part)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

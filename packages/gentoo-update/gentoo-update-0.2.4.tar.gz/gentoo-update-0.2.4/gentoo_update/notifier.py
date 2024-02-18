"""Provides a Notifier to send update reports via email, IRC or mobile."""

import json
import os
import socket
import ssl
import time
import urllib.request
from sys import exit
from typing import List, Tuple

ACCEPTED_HTTP_CODES = [200, 202]
USE_SENDGRID = True
try:
    import sendgrid  # noqa: I005
    from sendgrid.helpers.mail import Content, Email, Mail, To  # noqa: I005
except ImportError:
    USE_SENDGRID = False


class Notifier:
    """Notifier class for sending update reports."""

    def __init__(self, notification_type: str, report: List, short=True) -> None:
        """Initialize Notifier class."""
        report = report[0:2] if short else report

        if notification_type == "email":
            if USE_SENDGRID:
                self.send_report_to_mail(report)
            else:
                print("sendgrid library is not installed")
                print("it can be installed from GURU overlay:")
                print("  emerge --ask dev-python/sendgrid")
        elif notification_type == "irc":
            self.send_report_to_irc(report)
        elif notification_type == "mobile":
            self.send_report_to_mobile(report)
        else:
            print("Unsupported authentication methods")
            print("Currently supporting: irc")
            print("Exiting...")

    def get_irc_vars(self) -> Tuple:
        """Get variables needed to send report to IRC chat from env."""
        channel = os.getenv("IRC_CHANNEL")
        botnick = os.getenv("IRC_BOT_NICKNAME")
        botpass = os.getenv("IRC_BOT_PASSWORD")
        if None not in (channel, botnick, botpass):
            return channel, botnick, botpass
        else:
            print("Undefined enviromental variable(s)")
            print("Define: IRC_CHANNEL, IRC_BOT_NICKNAME, IRC_BOT_PASSWORD")
            exit(1)

    def send_report_to_irc(self, report: List[str]) -> None:
        """Send the update report to IRC chat."""
        server = "irc.libera.chat"
        port = 6697
        channel, botnick, botpass = self.get_irc_vars()
        ssl_context = ssl.create_default_context()

        irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        irc = ssl_context.wrap_socket(irc, server_hostname=server)
        irc.connect((server, port))
        irc.send(f"USER {botnick} {botnick} {botnick} {botnick}\n".encode())
        irc.send(f"NICK {botnick}\n".encode())
        irc.send(f"PRIVMSG NickServ :IDENTIFY {botnick} {botpass}\n".encode())
        time.sleep(5)

        irc.send(f"JOIN {channel}\n".encode())
        for line in report:
            irc.send(f"PRIVMSG {channel} :{line}\n".encode())
            time.sleep(10)
        print("report sent, quitting...")

        irc.send(b"QUIT \n")
        irc.close()

    def get_mail_vars(self) -> Tuple:
        """Get variables to send report to email via SendGrid from env."""
        api_key = os.getenv("SENDGRID_API_KEY")
        send_to = os.getenv("SENDGRID_TO")
        send_from = os.getenv("SENDGRID_FROM")
        if None not in (api_key, send_to, send_from):
            return api_key, send_to, send_from
        else:
            print("Undefined enviromental variable(s)")
            print("Please define: SENDGRID_API_KEY, SENDGRID_TO, SENDGRID_FROM")
            exit(1)

    def send_report_to_mail(self, report: List[str]) -> None:
        """Send the update report to email via SendGrid."""
        api_key, send_to, send_from = self.get_mail_vars()
        sendgrid_client = sendgrid.SendGridAPIClient(api_key=api_key)
        subject = "Gentoo Linux Update Report"

        content = Content("text/plain", "\n".join(report))
        mail = Mail(Email(send_from), To(send_to), subject, content)
        mail_json = mail.get()

        response = sendgrid_client.client.mail.send.post(request_body=mail_json)  # type: ignore
        if response.status_code in ACCEPTED_HTTP_CODES:
            print("email was sent successfully!")
        else:
            print("email was not sent successfully, details:")
            print(response.headers)
            print(response.body)

    def send_report_to_mobile(self, report: List[str]) -> None:
        """Send the update report to mobile app."""
        token = os.getenv("GU_TOKEN")
        if not token:
            print("Token not found, please define GU_TOKEN env variable.")
            exit(1)
        update_status = report[1].split(": ")[1]
        update_content = report[2:]

        url = "https://us-central1-gentoo-update.cloudfunctions.net/checkTokenAndForwardData"
        headers = {"Content-Type": "application/json"}
        data = {
            "token": token,
            "update_status": update_status,
            "update_content": update_content,
        }

        data = json.dumps(data).encode("utf-8")

        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            print(response.status)
            print(response.read().decode("utf-8"))

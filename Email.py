import smtplib
from email.message import EmailMessage
import Constants as const

def success_send(exec_details):
    msg = EmailMessage()
    msg['Subject'] = "Successfully Executed Trade for " + exec_details["symbol"]

    msg_body = "Trade has executed.\n\n" + \
               "Bought " + exec_details["executed_amount"] + " of " + \
               exec_details["symbol"] + " at price of " + \
               exec_details["avg_execution_price"] + " per coin."
    msg.set_content(msg_body)
    send(msg)


def failure_send():
    msg = EmailMessage()
    msg['Subject'] = "Failed to execute trade. Killed Program"
    msg.set_content("")
    send(msg)

def send(msg):
    msg['From'] = const.from_address
    msg['To'] = const.to_address
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()
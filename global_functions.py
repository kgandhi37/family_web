import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def send_email(toaddr, subj, body):
	toaddr = toaddr
	fromaddr = 'kishen.gandhi.1990@gmail.com'
	subj = subj
	body = body
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = subj
	msg.attach(MIMEText(body, 'plain'))
	server = smtplib.SMTP('smtp.gmail.com', 587) # for gmail, change for other providers, server and port
	server.starttls()
	server.login(fromaddr, "__kisheng__")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
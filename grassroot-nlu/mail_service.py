from logger import rootLogger
import os
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def mail(message, subject, *emergency):
    try:
        file = open('logs/overflowBlock', 'r')
        raw_str = file.read()
        file.close()
        cycles = int(raw_str) 
        rootLogger.info('Detected %s previous cycles in overflowBlock.' % cycles)   	
        if cycles > 5 and not emergency:
        	rootLogger.error('More than 5 errors have occured in less than 30 seconds. Calling for emergency counter-measures.')
        	system_failure()
        else:
            current_files = os.listdir('./')
            if 'sysf' in current_files:
                rootLogger.info('Developer has been notified on system failure. Suppressing further notification.')
            else:
                from_addr = os.environ['NLU_MAIL_ADDR']
                to_addr = os.environ['DEV']
                rootLogger.info('sending "%s..." to developer.' % message[:5])
                msg = MIMEMultipart()
                msg['From'] = from_addr
                msg['To'] = to_addr
                msg['Subject'] = subject
                body = message
                msg.attach(MIMEText(body, 'plain'))
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls() 
                server.login(from_addr, os.environ['NLU_MAIL_PWD'])
                text = msg.as_string()
                server.sendmail(from_addr, to_addr, text)
                server.quit()
                rootLogger.info('developer notified.')
                cycles += 1
                file = open('logs/overflowBlock', 'w')
                file.write(str(cycles))
                file.close()
    except Exception as e:
        rootLogger.error('failed to notify developer.')
        rootLogger.debug(str(e))


def system_failure():
    states = os.listdir('./')
    text = 'We have a giant boogy on the loose. Its time to go bug hunting.'
    if 'sysf' not in states:
        mail(text, 'System Failure', *['oh the horror'])
        os.system('touch sysf')
    else:
    	rootLogger.info('Developer has been notified on system failure. Suppressing further notification.')

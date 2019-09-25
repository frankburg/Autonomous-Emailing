def sendmail(email_receivers,indicator,orgUnit,value,period):
    """
    email_receivers:dict of first name and email of receivers
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from socket import gaierror
    from html_email.email import html
    """
    indicator=kwargs.get('indicator')
    period=kwargs.get('period')
    orgUnit=kwargs.get('orgUnit')
    value=kwargs.get('value')
    """

    login= "thefrankburg@gmail.com"
    password = "20001994" 
    sender_email = "thefrankburg@gmail.com"
    
    for name , em in email_receivers.items():
        receiver_email = em

        message = MIMEMultipart("alternative")
        message["Subject"] = "NMDR Critical Alert"
        message["From"] = sender_email
        message["To"] = receiver_email

        # write the plain text part
        text = """\
        Hi %s,
        Check out the new changes on your DHIS2 instanceThere is critical change in the data received in the NMDR       instance. The data value of %s, %s , received for the period of %s for the state, %s was above the normal. Please, click link below  to get all the details of the changes. This is it
        https://malaria.dhis2nigeria.org.ng/dhis/dhis-web-dashboard/
        Feel free to let us know if this info as useful to you!"""%(name,indicator,value,orgUnit,period)

        # write the HTML part
        ht=html(name,indicator,orgUnit,period,value)
        html =ht

        # convert both parts to MIMEText objects and add them to the MIMEMultipart message
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)


        try:

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(login,password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.close()

            # telling the script to report if your message was sent or which errors need to be fixed 
            print(f'Sent to {name}')
        except (gaierror, ConnectionRefusedError):
            print('Failed to connect to the server. Bad connection settings?')
        except smtplib.SMTPServerDisconnected:
            print('Failed to connect to the server. Wrong user/password?')
        except smtplib.SMTPException as e:
            print('SMTP error occurred: ' + str(e))
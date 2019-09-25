# Autonomous-Emailing
 This repo shows the autonomous triggering of an emailing system dependent on an action. When the value in the query from an API is above a threshold it triggers the sendmail function. The repo containing a python script for email set-up for Gmail and Outlook servers.
 
 The email.py contains the HTML formatting of the email. sendemail or sendemailOutlook sends email for Gmail or Outlook respectively.
 
         NMDR_email
              |
     sendemail or sendemailOutlook
              |
            email
              

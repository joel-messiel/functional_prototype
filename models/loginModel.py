from datetime import datetime, timedelta
import ssl
from flask import session, url_for
from connectDB import *
from passlib.hash import sha256_crypt
import smtplib
import pyotp
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import flash
from dotenv import load_dotenv
import os

load_dotenv()

# Email configuration
EMAIL_HOST = 'smtp.gmail.com'
# For ssl
EMAIL_PORT = 465
# Sender email
EMAIL_USER = os.getenv('EMAIL_USER')
# App password
APP_PASSWORD = os.getenv('APP_PASSWORD')

def send_verification_email(admin_email, admin_name, user_name, verification_url):
    """Send verification email with TOTP link"""
    subject = "Password Change Request - CoopManatí"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd;">
            <h2 style="color: #333f48;">Password Change Request</h2>
            <p>Hello {admin_name},</p>
            <p>{user_name} has requested to change their password. Please click the button below to authorize the password change:</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{verification_url}" style="background-color: #C8AC64; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">Authorize Password Change</a>
            </div>
            <p>This link will expire in <strong>30 minutes</strong> for security reasons.</p>
            <p>If you do not wish to authorize this change, please ignore this email.</p>
            <p>Don't share this email with anyone.</p>
            <br>
            <p style="color: #666;">Best regards,<br>CoopManatí System Team</p>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Password Change Request - CoopManatí
    
    Hello {admin_name},
    
    {user_name} has requested to change their password. Please click the button below to authorize the password change:
    
    {verification_url}
    
    This link will expire in 30 minutes for security reasons.
    
    If you do not wish to authorize this change, please ignore this email.
    
    Best regards,
    CoopManatí System Team
    """
    if not EMAIL_USER or not APP_PASSWORD:
        return False
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_USER
        msg['To'] = admin_email
        
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
            server.login(EMAIL_USER, APP_PASSWORD)
            server.sendmail(EMAIL_USER, admin_email, msg.as_string())

        
        print(f"Verification email sent to {admin_email}")
        return True
        
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
    

def loginModel(email, password):
    user = None
    db = Dbconnect()
    sql = "SELECT * FROM employee WHERE email = %s"
    # Save user info in list
    try:
        res = db.select(sql, (email))[0]
        user = {
            "employee_id": res['employee_id'], 
            "email": res['email'],
            "first_name": res['first_name'],
            "last_name": res['last_name'], 
            "password": res['password'], 
            "is_active": res['is_active'],
            "role": res['role']
        }
    
    except Exception as e:
        # Email not found
        print("Exception in loginmodel: ", e)
        return -1

    # sha256_crypt.hash("password") = this is what is used to encrypt a password
    # sha256_crypt.verify(password_unhashed, password_hashed) = this is what is used to compare an unhashed and hashed password

    if sha256_crypt.verify(password, user['password']) is True:
        if user['is_active'] == 0:
            # If the user is not active, return false
            flash("User is not active")
            return -1
        
        full_name = f"{user['first_name']} {user['last_name']}"
        # If the user is found, save the user ID in the session 
        session['username'] = user['employee_id']
        # Create the session['customer'] saving the customer ID if user is found
        session['userfullname'] = full_name

        # Store the role in session 
        if user['role'] == 'branch_admin':
            session['role'] = 'Administrador de Sucursal'
        elif user['role'] == 'general_admin':
            session['role'] = 'Administrador General'
        elif user['role'] == 'employee':
            session['role'] = 'Empleado'
           
    
        return 1
    
    else:
        # If it didn't find user, return false
        # flash("Invalid email or password", "error")
        return -1
    

def changePasswordModel(email, new_password, confirm_new_password):
    user = None
    db = Dbconnect()
    sql = "SELECT * FROM employee WHERE email = %s"
    # Save user info in list
    try:
        res = db.select(sql, (email))[0]
        # Constructing name from First, middle and last
        employee_name = ' '.join(filter(None, [
            res['first_name'],
            res['middle_initial'],
            res['last_name']
        ]))

        user = {
            "employee_id": res['employee_id'], 
            "name": employee_name,
            "email": res['email'], 
            "password": res['password'], 
            "is_active": res['is_active'],
            "role": res['role'],
            "branch_id": res['branch_id']
        }
    
    except Exception as e:
        # Email not found
        print("Exception: ", e)
        return -1
    
   
    if new_password == confirm_new_password:
        if user['is_active'] == 0:
            # If the user is not active, return false
            flash("User is not active", "error")
            return -1
        
        hashed_new_password = sha256_crypt.hash(new_password)
        # Generate TOTP secret and token
        totp_secret = pyotp.random_base32()
        totp = pyotp.TOTP(totp_secret, interval=1800)  # 30 minutes
        verification_token = totp.now()
        
        # Store in database with expiration
        expires_at = datetime.now() + timedelta(minutes=15)
        
        sql ="""INSERT INTO password_reset (password_reset_token, token_secret, token_expires, employee_id, new_password)
                VALUES (%s, %s, %s, %s, %s)"""
        
        try:
            db.execute(sql, (verification_token, totp_secret, expires_at, user['employee_id'], hashed_new_password))
            # Generate verification URL
            verification_url = url_for(
                'verify_password_reset', 
                email=email,
                token=verification_token,
                _external=True
            )

            email_sent = None
            # Send verification email
            if user['role'] == "branch_admin" or user['role'] == "general_admin":
                # authorization emails for admins are sent to themselves
                email_sent = send_verification_email(user['email'], user['name'], user['name'], verification_url)
                if email_sent:
                    flash('Verification email sent! Please check your inbox.', 'success')
                else:
                    flash('Failed to send email. Please try again.', 'error')

            else:
                # authorization emails for employees are sent to their respective admins
                admins = []
                sql = "SELECT email, first_name, middle_initial, last_name FROM employee WHERE role='branch_admin' or role='general_admin' and branch_id=%s"
                results = db.select(sql, (user['branch_id']))
    
                for res in results:
                    admin_name = ' '.join(filter(None, [
                        res['first_name'],
                        res['middle_initial'],
                        res['last_name']
                    ]))
                    admins.append((res['email'], admin_name))
                
                for admin_email, admin_name in admins:
                    email_sent = send_verification_email(admin_email, admin_name, user['name'], verification_url)

                if email_sent:
                    flash('Authorization email sent to administrators', 'success')
                else:
                    flash('Failed to send email to administrators. Please try again.', 'error')

        except Exception as e:
            print("Exception: ", e)
            # TODO: Maybe add another return code for unexpected errors
            return -1
    
    else:
        return -2
    
def deletePasswordResetEntry(token):
    db = Dbconnect()
    try:
        sql = "DELETE FROM password_reset WHERE password_reset_token = %s"
        db.execute(sql, (token))

    except Exception as e:
        print("Exception: ", e)
        return False 

def verifyPasswordResetModel(email, token):
    db = Dbconnect()
    res = None
    try:
        sql = "SELECT * FROM password_reset WHERE password_reset_token = %s"
        res = db.select(sql, (token))[0]
        deletePasswordResetEntry(token)
    
    except Exception as e:
        print("Exception: ", e)
        deletePasswordResetEntry(token)
        return False
    
    if not res:
        flash('Invalid or expired verification link', 'error')
        return False
    
    # Check if token expired
    if datetime.now() > res['token_expires']:
        flash('Verification link has expired. Please request a new one.', 'error')
        return False
    
    # Verify TOTP token
    totp = pyotp.TOTP(res['token_secret'], interval=1800)
    if not totp.verify(token, valid_window=1):  # Allow 1 step window
        flash('Invalid verification token', 'error')
        return False
    
    try:
        sql = """UPDATE employee  
                SET `password` = %s
                WHERE email = %s
        """
        res = db.execute(sql, (res['new_password'], email))
    
    except Exception as e:
        print("Exception: ", e)
        return False 

    return True
    
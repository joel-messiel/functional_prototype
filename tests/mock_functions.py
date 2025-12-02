from datetime import datetime, timedelta
from connectDB import *
from passlib.hash import sha256_crypt
import pyotp

def mockChangePasswordModel(email, new_password, confirm_new_password):
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
            #flash("User is not active", "error")
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
            # simulating verification url
            verification_url = "http://127.0.0.1:5003/reset_password" 
            # Generate verification URL
            """
            verification_url = url_for(
                'verify_password_reset', 
                email=email,
                token=verification_token,
                _external=True
            )
            """

            email_sent = None
            # Send verification email
            if user['role'] == "branch_admin" or user['role'] == "general_admin":
                # Simulating email being sent to administrator
                email_sent = True 

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
                
                # Simulating email being sent to administrator
                email_sent = True 

        except Exception as e:
            print("Exception: ", e)
            # TODO: Maybe add another return code for unexpected errors
            return -1
    
    else:
        return -2
    
    return 1
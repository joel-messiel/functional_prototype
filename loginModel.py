from flask import session
from connectDB import *
from passlib.hash import sha256_crypt
from flask import flash

def loginmodel(email, password):
    user = None
    db = Dbconnect()
    sql = "SELECT * FROM employee WHERE email = %s"
    # Save user info in list
    try:
        res = db.select(sql, (email,))[0]
        user = {
            "employee_id": res['employee_id'], 
            "email": res['email'], 
            "password": res['password'], 
            "is_active": res['is_active'],
            "role": res['role']
        }
    
    except Exception as e:
        print("Exception: ", e)
        return -1

    # sha256_crypt.hash("password") = this is what is used to encrypt a password
    # sha256_crypt.verify(password_unhashed, password_hashed) = this is what is used to compare an unhashed and hashed password

    if sha256_crypt.verify(password, user['password']) is True:
        if user['is_active'] == 0:
            # If the user is not active, return false
            flash("User is not active")
            return -1
        # If the user is found, save the user ID in the session 
        session['username'] = user['employee_id']
        # Create the session['customer'] saving the customer ID if user is found
        if user["role"] == "employee":
            return 2
        
        return 1
    
    else:
        # If it didn't find user, return false
        flash("Invalid email or password")
        return -1
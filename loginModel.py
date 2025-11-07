from flask import session
from connectDB import *
from passlib.hash import sha256_crypt
from flask import flash

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
            "password": res['password'], 
            "is_active": res['is_active'],
            "role": res['role']
        }
    
    except Exception as e:
        print("Exception in loginmodel: ", e)
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
    
def changePasswordModel(email, old_password, new_password):
    user = None
    db = Dbconnect()
    sql = "SELECT * FROM employee WHERE email = %s"
    # Save user info in list
    try:
        res = db.select(sql, (email))[0]
        user = {
            "employee_id": res['employee_id'], 
            "email": res['email'], 
            "password": res['password'], 
            "is_active": res['is_active'],
            "role": res['role'],
            "branch_id": res['branch_id']
        }
    
    except Exception as e:
        print("Exception: ", e)
        return -1
    
    if sha256_crypt.verify(old_password, user['password']) is True:
        if user['is_active'] == 0:
            # If the user is not active, return false
            flash("User is not active")
            return -1
        
        if user["role"] == "branch_admin" or user["role"] == "branch_admin":
            sql = "UPDATE employee SET password=%s WHERE employee_id=%s"
            try:
                hashed_new_password = sha256_crypt.hash(new_password)
                db.execute(sql, (hashed_new_password, user["employee_id"]))

            except Exception as e:
                print("Exception in changePasswordModel: ", e)
                return -1
            
            return 1

        else:
            # send email to manager
            # query a join between employee and branch where branch == employee branch and role == branch_admin
            # send email to result of that query
            return 2
    
    else:
        flash("Invalid password")
        return -1
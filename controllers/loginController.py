from models.loginModel import *
from flask import request, flash, redirect, render_template, session, url_for

def loginController(email, password):
    result = loginModel(email=email, password=password)
    # Check from loginModel's loginmodel() if user exists

    if 'request' in session:
        prev_page = session['request']
        session.pop('request', None)
        return redirect(prev_page)

    if result == 1:
        # admin page
        return redirect(url_for('dashboard'))
    
    elif result == 2:
        # employee page
        return redirect(url_for('dashboard'))
        return redirect(url_for('employee_page'))
    
    else:
        # If user doesn't exist, return to login and trigger error message
        flash('Invalid email or password', 'error')
        return render_template('login.html')
    
def changePasswordController(email, new_password, confirm_new_password):
    res = changePasswordModel(email, new_password, confirm_new_password)
    if res == -1:
        flash('Invalid email or password', 'error')
        return render_template('change_password.html')

    elif res == -2:
        flash('New passwords do not match')
        return render_template('change_password.html')

    return render_template('login.html')

def verifyPasswordResetController(email, token):
    return verifyPasswordResetModel(email, token)
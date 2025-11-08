from models.loginModel import *
from flask import redirect, render_template, session, url_for
from passlib.hash import sha256_crypt


def loginController(email, password):
    result = loginModel(email=email, password=password)
    # Check from loginModel's loginmodel() if user exists

    if 'request' in session:
        request = session['request']
        session.pop('request', None)
        return redirect(request)

    if result == 1:
        # admin page
        return redirect(url_for('dashboard'))
        return redirect(url_for('admin_page'))
    
    elif result == 2:
        # employee page
        return redirect(url_for('employee_page'))
    
    else:
        # If user doesn't exist, return to login and trigger error message
        return render_template('login.html', error='Invalid username or password')
    
def changePasswordController(email, old_password, new_password):
    res = changePasswordModel(email, old_password, new_password)
    message = ''
    if res == -1:
        message = 'Invalid username or password'

    elif res == 1:
        flash('Password was successfully changed')

    else:
       flash('A link was sent to your branch manager in order to reset your password')

    return render_template('login.html', error=message)
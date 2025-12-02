from models.loginModel import *
from flask import request, flash, redirect, render_template, session, url_for

def loginController(email, password):
    result = loginModel(email=email, password=password)
    # Check from loginModel's loginmodel() if user exists

    if 'request' in session:
        prev_page = session['request']
        session.pop('request', None)
        return redirect(prev_page)
    
    if not result:
        # If user doesn't exist, return to login and trigger error message
        flash('Invalid email or password', 'error')
        return render_template('login.html')
    
    full_name = f"{result['first_name']} {result['last_name']}"
    # If the user is found, save the user ID in the session 
    session['username'] = result['employee_id']
    # Create the session['customer'] saving the customer ID if user is found
    session['userfullname'] = full_name

    # Store the role in session 
    if result['role'] == 'branch_admin':
        session['role'] = 'Administrador de Sucursal'
    elif result['role'] == 'general_admin':
        session['role'] = 'Administrador General'
    elif result['role'] == 'employee':
        session['role'] = 'Empleado'

    if session['role'] == 'Empleado':
        # employee page
        return redirect(url_for('dashboard'))
        return redirect(url_for('employee_page'))

    else:
        # admin page
        return redirect(url_for('dashboard'))
    
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
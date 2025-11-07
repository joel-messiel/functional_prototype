from loginModel import *
from flask import redirect, render_template, session, url_for
from passlib.hash import sha256_crypt


def logincontroller(email, password):
    result = loginmodel(email=email, password=password)
    # Check from loginModel's loginmodel() if user exists

    if 'request' in session:
        request = session['request']
        session.pop('request', None)
        return redirect(request)

    if result == "true":
        # If user exists, enter shop
        #return redirect("/shop")
        return redirect(url_for('dashboard'))
    else:
        # If user doesn't exist, return to login and trigger error message
        return render_template('login.html', error='Invalid username or password')
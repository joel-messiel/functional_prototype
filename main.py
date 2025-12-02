from flask import Flask, render_template, request, redirect, url_for, session
from controllers.loginController import *
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Routes
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        return loginController(email, password)

    return render_template('login.html')


# this will be changed to change password
@app.route('/change_pass', methods=['GET', 'POST'])
def change_pass():
    if request.method == 'POST':
        username = request.form['email']
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')
        return changePasswordController(username, new_password, confirm_new_password)
    return render_template('change_password.html')


@app.route('/verify-password-reset')
def verify_password_reset():
    # requester's email
    email = request.args.get('email')
    # verification token
    token = request.args.get('token')
    
    verifyPasswordResetController(email, token)
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():

    # Remove from session the following data
    session.pop('username', None)
    session.pop('role', None)
    session.pop('userfullname', None)
    return redirect(url_for('login'))

# TEMPORARY : Since the pause and profile page arent implemented i redirected to this
@app.route('/not_found', methods=['GET', 'POST'])
def not_found():
      return render_template('not_found.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html')


# Run the application
if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, request, redirect, url_for, session
import json
from werkzeug.security import check_password_hash, generate_password_hash
from controllers.loginController import loginController, changePasswordController
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
def signup():
    if request.method == 'POST':
        username = request.form['email']
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')
        print("ok")
        return changePasswordController(username, old_password, new_password, confirm_new_password)
    print("ok", request.method)
    return render_template('change_password.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


# Run the application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

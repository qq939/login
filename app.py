from flask import request, render_template, redirect, url_for, flash
from models import app, get_user_by_username

# Secret key is needed for session/flash
app.secret_key = 'some_secret_key'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = get_user_by_username(username)
        
        if user and user.password == password:
            return "Login successful"
        else:
            flash("Invalid credentials")
            return render_template('login.html'), 401
            
    return render_template('login.html')

@app.route('/')
def index():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5025, debug=True)

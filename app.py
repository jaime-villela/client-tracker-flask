from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
# from flask_sqlalchemy import SQLAlchemy  #  If you're using a database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  #  Change this!
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:// /users.db'  #  Example SQLite  database
# db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  #  Where to redirect users who need to log in

# --- User  Model (Simplified) ---
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# --- Load User Callback ---
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/")
def home():
    #return "Welcome to my Flask app!"
    return redirect(url_for('login'))

# --- Login Route ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #  **VERY  BASIC Authentication - Replace with a Proper System**
        if username == 'testuser' and password == 'password':
            user = User(username)  #  Use username as ID
            login_user(user)
            return redirect(url_for('protected'))  #  Redirect to a protected page
        else:
            return 'Invalid credentials'
    return render_template('login.html')  #  Create a login.html template

# --- Logout Route ---
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- Protected Route ---
@app.route('/protected')
@login_required
def protected():
    return f'Logged in as: {current_user.id}'

if __name__ == '__main__':
    app.run(debug=True) 

from flask import Blueprint, flash, g, redirect, render_template, request, url_for, session
from werkzeug.exceptions import abort
from urllib.parse import urlparse
#from hyprnews.auth import login_required
from .models import Article, User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@bp.route('/register', methods=('GET', 'POST'))
def register():

    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']
        error    = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        # TODO: is it a vaild email address?

        if error is None:
            # TODO - attempt to load this user - are they registered?
            # User.get_by_email("bob@example.com")
            # If this user exists:
            # error = f"User {username} is already registered."
            u = User(email=email) # TODO hash password and add it here
            u.save()
            #
            #
            return redirect(url_for("auth.login"))
            #
            #
            
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        # TODO:
        # 1 hash password
        # 2 check password hash matches hash in DB
        #   using check_password_hash()

        email = request.form['email']
        print(email)
        u = User.get_by_email(email)
        if u:
            print(u)

            session.clear()
            #session['user_id'] = user['id']
            session['user_id'] = u.id
            return redirect(url_for('index'))
        else:
            error = "Email or password incorrect"
            
        flash(error)

    return render_template('auth/login.html')
"""
This file contains routes for the pages related to logging in.

:author William Boyles:
"""

from flask import Blueprint, render_template, request, redirect, session

# Most view classes shouldn't work so directly with persistence classes
from ...persistent.user.user import User

login_view_controller = Blueprint("login_view_controller",
                                  __name__,
                                  template_folder="templates",
                                  static_folder="static",
                                  url_prefix="/")

BASE_FILE_URL = "login/"


@login_view_controller.route("/", methods=['GET'])
def redirect_to_login():
    return redirect("/login")


# Most view methods wouldn't have a POST
@login_view_controller.route("/login", methods=['GET', 'POST'])
def login_home():
    # User is filling out login form
    if request.method == 'POST':
        session.pop('username', None)
        session.pop('password_hash', None)
        session.pop('role', None)

        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            db_user = User.query.filter(User.username == username).first()
            if db_user and db_user.check_password(password):
                session['username'] = username
                session['password_hash'] = db_user.password_hash
                session['role'] = db_user.role.role_name

                return redirect(db_user.role.landing_page)

    # If user already has a session, verify it matches a db user and log in
    session_username = session.get('username')
    session_password = session.get('password_hash')
    if session_username and session_password:
        db_user = User.query.filter(User.username == session_username).first()
        if db_user.password_hash == session_password:
            return redirect(db_user.role.landing_page)

    # Otherwise, show login page
    return render_template(BASE_FILE_URL + "login.html")


@login_view_controller.route("/logout", methods=['GET'])
def logout():
    session.pop('username', None)
    session.pop('password_hash', None)
    session.pop('role', None)

    return render_template(BASE_FILE_URL + "login.html")
import os

from flask import render_template, request, redirect, url_for, abort, make_response

from utils.decorators import public_handler

@public_handler
def index(**params):
    return render_template("public/index.html", **params)

@public_handler
def login(**params):
    if request.method == "GET":
        return render_template("public/login.html", **params)

    elif request.method == "POST":
        username = request.form.get("login-username")
        password = request.form.get("login-password")

        if username and password:
            # find a User with this username (if it doesn't exist: 404)
            user = User.get_by_username(username=username)

            if not user:
                return abort(404)

            # check if passwords match (if not: 403)
            if User.is_password_valid(user=user, password=password):
                # if passwords match, generate a session token and save its hash in the database
                session_token = User.generate_session_token(user=user, request=request)

                # prepare a response and then store the token in a cookie
                response = make_response(redirect(url_for("tasks.my_tasks")))

                # on localhost don't make the cookie secure and http-only (but on production it should be)
                cookie_secure_httponly = False
                if os.getenv('GAE_ENV', '').startswith('standard'):
                    cookie_secure_httponly = True

                # store the token in a cookie
                response.set_cookie(key="ninja-todo-session", value=session_token, secure=cookie_secure_httponly,
                                    httponly=cookie_secure_httponly)
                return response

        return abort(403)

@public_handler
def register(**params):
    if request.method == "GET":
        return render_template("public/register.html", **params)

    elif request.method == "POST":
        firstname = request.form.get("login-username")
        lastname = request.form.get("login-username")
        username = request.form.get("login-username")
        password = request.form.get("login-password")

        if username and password and firstname and lastname:
            # find a User with this username (if it doesn't exist: 404)
            user = User.get_by_username(username=username)

            if not user:
                return "success"

        return abort(403)
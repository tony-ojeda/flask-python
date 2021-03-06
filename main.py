import unittest
from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from app import create_app
from app.forms import LoginForm
from flask_login import login_required, current_user
from app.firestore_service import  get_users, get_todos

app = create_app()

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def internalr_server_error(error):
    return render_template('500.html',error=error)

@app.route('/')
def index():
    user_id = request.remote_addr

    response = make_response(redirect('/hello'))
    # response.set_cookie('user_id', user_id)
    session['user_id'] = user_id

    return response

@app.route('/hello',methods=['GET'])
@login_required
def hello():
    # user_id = request.cookies.get('user_id')
    user_id = session.get('user_id');
    username = current_user.id

    context = {
        'user_id':user_id,
        'todos':get_todos(user_id=username),
        'username': username
    }

    return render_template('hello.html',**context)


from functools import wraps
from flask import Flask, render_template, redirect, url_for, flash, get_flashed_messages, make_response, abort, request
from flask_login import login_user, logout_user, login_required, UserMixin, LoginManager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

from google.cloud import datastore
import logging # GAE uses default Python logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e8cd8d39fc24df015d7ab545'
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

CLOUD_STORAGE_BUCKET =  'final_project_bucket1'


# API key decorator
def require_api_key(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    print(request.headers)
    if request.headers.get('X-Api-Key') != "abcdef123456":
      abort(401)
    return f(*args, **kwargs)
  return decorated_function


"""400 Bad request"""
@app.errorhandler(400)
def bad_request():
  """Bad request."""
  return make_response("Bad request", 400)

"""404 Error Page"""
@app.errorhandler(404)
def page_not_found(e):
    return "Page not found.", 404


@app.route('/analytics/')
@app.route('/analytics/home')
def home_page():
    return render_template('home.html')


@app.route('/analytics//login', methods=['GET', 'POST'])
def login_page():
    # create datastore client
    datastore_client = datastore.Client.from_service_account_json('finalproject-351111-6daf7b7b781a.json')
    form = LoginForm()
    if form.validate_on_submit():
        # query through the database and find if there is a username present
        query = datastore_client.query(kind='Admin')
        query.add_filter('username', '=', form.username.data)
        attempted_users = list(query.fetch())
        if attempted_users and attempted_users[0]['password'] == form.password.data:
            attempted_user = attempted_users[0]
            user_to_login = User(id=attempted_user['user_id'],
                                username=form.username.data,
                                password=form.password.data)             
            login_user(user_to_login)
            flash(f'Success! You are logged in as: {user_to_login.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/analytics/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))


@app.route('/analytics/dashboard', methods=['GET'])
def dashboard():
    datastore_client = datastore.Client.from_service_account_json('finalproject-351111-6daf7b7b781a.json')
    query = datastore_client.query(kind='Analytics')
    analytic = list(query.fetch())[0]
    return render_template('dashboard.html', analytic=analytic)


# data models ------------------------------------------------------------------------------

@login_manager.user_loader
def load_user(user_id):
    # create datastore client
    datastore_client = datastore.Client.from_service_account_json('finalproject-351111-6daf7b7b781a.json')
    query = datastore_client.query(kind='Admin')
    query.add_filter('user_id', '=', int(user_id))
    print(f"user id is: {user_id}")
    datas = list(query.fetch())
    if datas:
        data = datas[0]
        user = User(data['user_id'], data['username'], data['password'])
        return user
    else:
        user = User(0, 'admin', 'password')
        return user


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password



# forms module ---------------------------------------------------------------------------

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


if __name__ == '__main__':
    app.run(debug=True)


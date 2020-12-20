import flask
from . import flask_app

# Роутинг
@flask_app.route('/')
def hello():
    return flask.render_template('index.html')

@flask_app.route('/dash-osv')
def render_dashboard():
    return flask.redirect('/dash_osv')

@flask_app.route('/reports')
def render_reports():
    return flask.redirect('/dash2')
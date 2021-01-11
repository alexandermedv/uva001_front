import flask
from . import flask_app

# Роутинг
@flask_app.route('/')
def hello():
    return flask.render_template('index.html')

# @flask_app.route('/limit_oper')
# def render_dashboard():
#     print('limit_oper')
#     return flask.redirect('/limit_oper1')

# @flask_app.route('/reports')
# def render_reports():
#     return flask.redirect('/dash2')
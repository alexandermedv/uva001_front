
import config

from werkzeug.serving import run_simple
# from front_ex.dashes import dispatch_app
from front_ex import dispatch_app


if(__name__ == '__main__'):
    run_simple('0.0.0.0', 9104, dispatch_app,  use_debugger=config.USE, use_reloader=True)    
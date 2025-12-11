import os, traceback, secrets

import sympy as sp
import pandas as pd
import numpy as np

from flask import Flask, render_template, request, jsonify, url_for
from itertools import count
from gunicorn.app.base import BaseApplication

def create_app():
    PORT = 5000
    SERVER_NAME = '127.0.0.1' + f':{PORT}'

    app = Flask(__name__)
    app.config['SERVER_NAME'] = SERVER_NAME
    app.config['DEBUG'] = True
    app.config['PORT'] = PORT
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024

    with app.app_context():
      url_for('static', filename='/scripts/main.js')
      url_for('static', filename='/scripts/home.js')
      url_for('static', filename='/scripts/mathjax.js')
      url_for('static', filename='/styles/main.css')
      url_for('static', filename='/styles/home.css')

    @app.route("/")
    def home():
      return render_template("index.html")

    @app.route("/about")
    def about():
      return render_template("about.html")

    @app.route("/help")
    def help():
      return render_template("help.html")

    @app.route("/api/newton-raphson/root", methods=["POST"])
    def newton_raphson_root():
      try:
        data = request.json
        f_input = data.get("function")
        initial_guess = float(data.get("initial_guess"))
        tolerance = float(data.get("tolerance"))

        x = sp.symbols('x')
        f = sp.parse_expr(f_input, transformations="all")
        deriv = sp.Derivative(f, x)

        x0 = initial_guess
        x1 = None

        iteration_table = pd.DataFrame(columns=["Iteration", "x", "f(x)", "f'(x)", "x1 - x0"])

        for i in count(1):
          f_x0 = f.evalf(n=11, subs={x: x0})
          deriv_f_x0 = deriv.doit().evalf(n=11, subs={x: x0})

          x1 = x0 - (f_x0 / deriv_f_x0)
          f_x1 = f.evalf(n=11, subs={x: x1})
          deriv_f_x1 = deriv.doit().evalf(n=11, subs={x: x1})

          gap = abs(x1 - x0)

          if i == 1:
              iteration_table.loc[i-1] = [i-1, np.float64(x0), np.float64(f_x0), np.float64(deriv_f_x0), 0]

          iteration_table.loc[i] = [i, np.float64(x1), np.float64(f_x1), np.float64(deriv_f_x1), np.float64(gap)]

          if gap < tolerance:
            return jsonify({
              "converged": True,
              "iterations": i,
              "root_approximation": np.float64(x1),
              "function_value_at_root": np.float64(f_x1),
              "derivative_value_at_root": np.float64(deriv_f_x1),
              "iteration_table": iteration_table.set_index("Iteration").to_dict(orient="index"),
              "message": "Root found for inputted function.",
              "status": 200
            })
          
          if i > 1000:
            return jsonify({
              "converged": False,
              "message": "Maximum iterations (1000) reached without convergence.",
              "status": 200            
            })

          x0 = x1

      except ValueError:
        err_log = open('./error.log', "at")
        err_log.write(f'\n{traceback.format_exc()}')
      
        return jsonify({
          "status": 500,
          "message": """Something is wrong with your input. Please ensure it is typed or copied as plain text and refer to
          the <a href="/help">help page</a> for more information.""",
        })
      
      except TypeError:
        err_log = open('./error.log', "at")
        err_log.write(f'\n{traceback.format_exc()}')

        return jsonify({
          "status": 500,
          "message": """Your function \\(f(x)\\) format is not supported. Please refer to 
          the <a href="/help">help page</a> for information on the supported function format."""
        })
      
      except Exception as exc:
        err_log = open('./error.log', "at")
        err_log.write(f'\n{traceback.format_exc()}')

        return jsonify({
          "status": 500,
          "message": "We were unable to process your result due to an internal error. Sorry, please try again later.",
        })

    return app

class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.application = app
        self.options = options or {}
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

def number_of_workers():
  return (os.cpu_count() or 1) * 2 + 1


app = create_app()
options = {
    'bind': f'{app.config["SERVER_NAME"]}',
    'workers': number_of_workers(),
    'accesslog': './access.log',
    'errorlog': './error.log',
    'timout': 30,
}
StandaloneApplication(app, options).run()
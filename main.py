from flask import Flask, render_template, request, jsonify, url_for
from itertools import count

import sympy as sp
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
  url_for('static', filename='/scripts/main.js')
  url_for('static', filename='/scripts/mathjax.js')
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/help")
def help():
  return render_template("help.html")

@app.route("/api/newton-raphson/root", methods=["POST"])
def newton_raphson_root():
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
        "root_approximation": np.float64(x1.evalf(n=11)),
        "iteration_table": iteration_table.set_index("Iteration").to_dict(orient="index"),
        "error": ""
      })
    
    if i > 1000:
      return jsonify({
        "converged": False,
        "message": "Maximum iterations (1000) reached without convergence.",
        "error": ""
      })

    x0 = x1

if __name__ == "__main__":
  app.run(debug=True)

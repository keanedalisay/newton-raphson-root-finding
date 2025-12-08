import pytest
import sympy as sp
import pandas as pd
import numpy as np

from itertools import count

def test_newton_raphson_root():
    data = newton_raphson_root({
        "function": "x^2 - 2",
        "initial_guess": 1.0,
        "tolerance": 1e-4
    })

    assert data["converged"] is True
    assert data["iterations"] > 0
    assert data["root_approximation"] == pytest.approx(1.41421356)
    assert data["function_value_at_root"] == pytest.approx(4.510835047657717e-12)
    assert data["derivative_value_at_root"] == pytest.approx(2.82842712)
    assert "iteration_table" in data

def newton_raphson_root(data):
  f_input = data["function"]
  initial_guess = float(data["initial_guess"])
  tolerance = float(data["tolerance"])

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
      return {
        "converged": True,
        "iterations": i,
        "root_approximation": np.float64(x1),
        "function_value_at_root": np.float64(f_x1),
        "derivative_value_at_root": np.float64(deriv_f_x1),
        "iteration_table": iteration_table.set_index("Iteration").to_dict(orient="index"),
        "error": ""
      }
    
    if i > 1000:
      return {
        "converged": False,
        "message": "Maximum iterations (1000) reached without convergence.",
        "error": ""
      }

    x0 = x1
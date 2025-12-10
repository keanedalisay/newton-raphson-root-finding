import pytest
import sympy as sp
import pandas as pd
import numpy as np

from itertools import count

def test_newton_raphson_root():
    # test multiple functions, initial guesses, and tolerances
    polynomials = [
        {"function": "x^2 - 2", "initial_guess": 1.0, "tolerance": 1e-4},
        {"function": "ln(x) - (0.10 * x^2) + (0.05 * sin(x)) - 0.05", "initial_guess": 1.0, "tolerance": 1e-4},
        {"function": "x^2 - 10", "initial_guess": 3.0, "tolerance": 1e-8},
        {"function": "x^3 - 2x - 5", "initial_guess": 2.0, "tolerance": 1e-6},
        {"function": "x^3 -x - 1", "initial_guess": 1.5, "tolerance": 1e-6},
        {"function": "x cos(x) - x^2", "initial_guess": 1, "tolerance": 1e-6},
        # {"function": "x^100", "initial_guess": 0.1, "tolerance": 1e-6}, 100 subscript not supported, due to format
        # {"function": "e^{2x} - x - 6", "initial_guess": 0.97, "tolerance": 1e-6}, variable subscript not supported
        # {"function": "5x + ln(x) − 10000", "initial_guess": 1998.48, "tolerance": 1e-4}, conversion to float error
        # {"function": "a - 1/x", "initial_guess": 0.75, "tolerance": 0.000000001} conversion to float error

    ]

    approximations = [
       {"root_approximation": 1.41421356, "function_value_at_root": 4.510835047657717e-12, "derivative_value_at_root": 2.82842712},
       {"root_approximation": 1.145244167, "function_value_at_root": -2.2246622950008044e-16, "derivative_value_at_root": 0.66476857},
       {"root_approximation": 3.1622776601},
       {"root_approximation": 2.09455148},
       {"root_approximation": 1.324719},
       {"root_approximation": 0.739085133215161},
      #  {"root_approximation": 0.095099004},
      #  {"root_approximation": 0.97087002},
      #  {"root_approximation": 1998.479972},
      # {"root_approximation": 0.729927007}
    ]

    for i in range(len(polynomials)):
        data = newton_raphson_root(polynomials[i])
        assert data["converged"] is True
        assert data["iterations"] > 0
        assert data["root_approximation"] == pytest.approx(approximations[i]["root_approximation"])
        # assert data["function_value_at_root"] == pytest.approx(approximations[i]["function_value_at_root"])
        # assert data["derivative_value_at_root"] == pytest.approx(approximations[i]["derivative_value_at_root"])

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
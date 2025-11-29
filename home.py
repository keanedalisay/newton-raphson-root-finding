from itertools import count

import streamlit as st
import sympy as sp
import pandas as pd

def home():
  st.title("Newton-Raphson Method for Root-Finding")

  st.divider()

  f_input = st.text_input("Enter the function f(x) for which you want to find the root.", value="x^2 -4x - 7")

  col1, col2 = st.columns(2)

  with col1:
    tolerance = st.number_input("Enter the tolerance level (e.g., 0.0001):", value=0.0001, format="%.10f")
  with col2:
    initial_guess = st.number_input("Enter the initial guess for the root:")

  find_root = st.button("Find the root", type="primary", use_container_width=True)

  st.divider()

  if find_root:
    progress_info = st.info("Finding root...")

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
          iteration_table.loc[i-1] = [i-1, x0, f_x0, deriv_f_x0, 0]

      iteration_table.loc[i] = [i, x1, f_x1, deriv_f_x1, gap]

      if gap < tolerance:
        progress_info.empty()
        st.header("Result")
        st.write(f"Converged at iteration {i} with root approximation: {x1.evalf(n=11)}")
        break

      x0 = x1
    
    st.table(iteration_table)

home()
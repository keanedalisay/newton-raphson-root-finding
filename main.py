from itertools import count

import streamlit as st
import sympy as sp

def cli_app():
  print("=== Newton-Raphson Method for Root-Finding ===")

  print("\nEnter the function f(x) for which you want to find the root.")
  x = sp.symbols('x')
  f = sp.parse_expr(input("f(x) = "), transformations="all")
  # f = ln(x) - (0.10 * x ** 2) + (0.05 * sin(x)) - 0.05
  tolerance = float(input("\nEnter the tolerance level (e.g., 0.0001): "))

  deriv = sp.Derivative(f, x)

  x0 = float(input("\nEnter the initial guess for the root: "))
  x1 = None

  # Newton-Raphson Method for Root-Finding
  print(f"\nIteration 0: x0 = {x0}, f(x0) = {f.subs(x, x0)}")
  for i in count(1):
    f_x0 = f.evalf(n=11, subs={x: x0})
    deriv_f_x0 = deriv.doit().evalf(n=11, subs={x: x0})

    x1 = x0 - (f_x0 / deriv_f_x0)

    print(f"Iteration {i}: x{i} = {x1}, f(x{i}) = {f.evalf(n=11, subs={x: x1})}")

    if abs(x1 - x0) < tolerance:
      print("\nConverged at iteration", i, "with root approximation: ", x1.evalf(n=11))
      break

    x0 = x1

def streamlit_app():
  st.title("Newton-Raphson Method for Root-Finding")

  st.write("Enter the function f(x) for which you want to find the root.")
  f_input = st.text_input("f(x) =", "x^2 -4x - 7")
  tolerance = st.number_input("Enter the tolerance level (e.g., 0.0001):", value=0.0001, format="%.10f")
  initial_guess = st.number_input("Enter the initial guess for the root:")

  if st.button("Find Root"):
    x = sp.symbols('x')
    f = sp.parse_expr(f_input, transformations="all")
    deriv = sp.Derivative(f, x)

    x0 = initial_guess
    x1 = None

    st.write(f"### Iteration 0: x0 = {x0}, f(x0) = {f.subs(x, x0)}")
    for i in count(1):
      f_x0 = f.evalf(n=11, subs={x: x0})
      deriv_f_x0 = deriv.doit().evalf(n=11, subs={x: x0})

      x1 = x0 - (f_x0 / deriv_f_x0)

      st.write(f"### Iteration {i}: x{i} = {x1}, f(x{i}) = {f.evalf(n=11, subs={x: x1})}")

      if abs(x1 - x0) < tolerance:
        st.write(f"### Converged at iteration {i} with root approximation: {x1.evalf(n=11)}")
        break

      x0 = x1

if __name__ == "__main__":
  streamlit_app()

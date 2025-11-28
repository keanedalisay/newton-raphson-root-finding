from itertools import count

import sympy as sp

def main():
  x = sp.symbols('x')
  f = sp.ln(x) - (0.10 * x ** 2) + (0.05 * sp.sin(x)) - 0.05
  tolerance = 1e-4

  deriv = sp.Derivative(f, x)

  x0 = 1
  x1 = None

  # Newton-Raphson Method for Root-Finding
  print(f"Iteration 0: x0 = {x0}, f(x0) = {f.subs(x, x0)}")
  for i in count(1):
    f_x0 = f.evalf(n=11, subs={x: x0})
    deriv_f_x0 = deriv.doit().evalf(n=11, subs={x: x0})

    x1 = x0 - (f_x0 / deriv_f_x0)

    print(f"Iteration {i}: x{i} = {x1}, f(x{i}) = {f.evalf(n=11, subs={x: x1})}")

    if abs(x1 - x0) < tolerance:
      print("Converged at iteration", i, "with root approximation: ", x1.evalf(n=11))
      break

    x0 = x1

if __name__ == "__main__":
  main()

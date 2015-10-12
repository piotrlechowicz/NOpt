# NewtonOpt
###Newton algorithm for the unconstrained task

Newton gradient algorithm for finding the minimum of a function of two variables.
Newton method is the second order method, it means it uses not only the gradient but also the hesian to find the minimum.

Pre-requirements:
* numpy
* py_expression_eval
* matplotlib

Newton algorithm is as follows:
There is a given function of two dimensions - f(x, y)
1. Given P0 = (x0, y0), set i = 0, set epsilon
2. dk := -H(Pi)^(-1) * grad(Pi)
3. If -dk < epsilon: stop
4. Choose step size tau_k := 1
5. Pk+1 := Pk + dk * tau_k, Go to 1.

Step 2 is augmented by a line-search of f(Pk + tau * dk) to find an optimal value of the step-size parameter tau.

Dk is a descent direction if H(Pk) is SPD (symetric and positive definite) and d != 0. It is sufficient to show that:
-grad(Pk)' * H(Pk)^(-1) * grad(Pk) < 0.

If H(Pk) is not SPD or there is impossible to calculate inverse matrix of H(Pk) than to calculate next step is used Steepest Descent Algorithm.









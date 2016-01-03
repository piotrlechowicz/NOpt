# NewtonOpt
###Newton algorithm for the unconstrained task

Newton gradient algorithm for finding the minimum of a function of two variables.
Newton method is the second order method, it means it uses not only the gradient but also the hessian to find the minimum.

Pre-requirements:
* numpy==1.10.1
* py_expression_eval
* matplotlib=1.5.0
* scipy==0.13.3
* PyQt5

#####Newton algorithm is as follows:
There are given parameters set by the user:

1. `P0` - starting point for the algorithm
2. `epsilon` - tolerance of the solution 

Meaning of the symbols in the algorithm:

1. `Pi` - point in which is considered minimum in the i-th iteration
2. `tau` - size of the movement step; it is calculated based on different algorithm - Golden Section Search
3. `dk` -  direction of next step

There is a given function of two dimensions - `f(x, y)`

1. Given `P0 = (x0, y0)`, set `i = 0`, set `epsilon`
2. `dk := -H(Pi)^(-1) * grad(Pi)`
3. Choose step size `tau_k` (optimization in direction)
4. `Pk+1 := Pk + dk * tau_k`, Go to 1.
5. `If Pk+1 - Pk < epsilon; then STOP; else i += 1, go to 2

Step 4 is augmented by a line-search of `f(Pk + tau * dk)` to find an optimal value of the step-size parameter `tau`.

`dk` is a descent direction if `H(Pk)` is SPD (symmetric and positive definite) and `dk != 0`. It is sufficient to show that:
`-grad(Pk)' * H(Pk)^(-1) * grad(Pk) < 0`.

If `H(Pk)` is not SPD or there is impossible to calculate inverse matrix of `H(Pk)` than to calculate next step is used Steepest Descent Algorithm.









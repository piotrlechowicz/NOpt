# NewtonOpt
###Newton algorithm for the unconstrained task

Newton gradient algorithm for finding the minimum of a function of two variables.
Newton method is the second order method, it means it uses not only the gradient but also the hessian to find the minimum.

###1. Pre-requirements:

|*Package*|*Version*|
|---|---|
|numpy | 1.10.1 |
|py_expression_eval| |
|matplotlib | 1.5.0 |
|scipy | 0.13.3 |
|PyQt5 | |

###2. Algorithm's description
#####2.1 Constants (input parametrs):

* `P0` - starting point for the algorithm
* `epsilon` - tolerance of the solution
* `f(x, y)` - function of two dimensions
 
#####2.2 Variables:

* `Pi` - point in which is considered minimum in the i-th iteration
* `tau` - size of the movement step; it is calculated based on different algorithm - Golden Section Search
* `dk` -  direction of next step

#####2.3 Pseudocode:

```
1.  given:  P_0 = (x0, y0)  # starting point
            i = 0           # iteration
            epsilon         # tolerance
2.  d_k := -H(P_i)^(-1) * grad(P_i)
3.  choose step size tau_k (optimization in direction)
4.  P_k+1 := P_k + d_k * tau_k 
5.  if P_k+1 - P_k < epsilon:
      then STOP
6.  else: 
      i += 1 and go to step *2*
```

Step 4 is augmented by a line-search of `f(Pk + tau * dk)` to find an optimal value of the step-size parameter `tau`.

`dk` is a descent direction if `H(Pk)` is SPD (symmetric and positive definite) and `dk != 0`. It is sufficient to show that:
`-grad(Pk)' * H(Pk)^(-1) * grad(Pk) < 0`.

If `H(Pk)` is not SPD or there is impossible to calculate inverse matrix of `H(Pk)`. Therefore to calculate next step the Steepest Descent Algorithm is used.

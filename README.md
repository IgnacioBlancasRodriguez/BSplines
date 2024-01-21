# BSplines in Python

The following project explores the world of bsplines or basic splines, specifically uniform and open uniform splines with the goal of achieving $C^2$ continuity. One of the optimizations made in the project is the use of memoization for the calculation of the basis functions.

## 1. Matrix form $C^2$ continuous BSpline
The first curve in the project is one where the basis functions are uniform across the whole curve. In order to simplify computation, these basis functions are precomputed to guarantee $C^2$ continuity by solving a system of $16x16$ equations that relate the corresponding functions and their first and second derivatives. This system, then yields a solution, which we express in the form of a matrix, where each column represents the coefficients of each basis function,
```math
\begin{bmatrix}
    \frac{1}{6} & \frac{2}{3} & \frac{1}{6} & 0 \\
    \frac{-1}{2} & 0 & \frac{1}{2} & 0 \\
    \frac{1}{2} & -1 & \frac{1}{2} & 0 \\
    \frac{-1}{6} & \frac{1}{2} & \frac{-1}{2} & \frac{1}{6}
\end{bmatrix}
```
We then achieve the following Spline function (in matrix form),
```math
P(t)=
\begin{bmatrix}
    1 & t & t^2 & t^3
\end{bmatrix}
\begin{bmatrix}
    \frac{1}{6} & \frac{2}{3} & \frac{1}{6} & 0 \\
    \frac{-1}{2} & 0 & \frac{1}{2} & 0 \\
    \frac{1}{2} & -1 & \frac{1}{2} & 0 \\
    \frac{-1}{6} & \frac{1}{2} & \frac{-1}{2} & \frac{1}{6}
\end{bmatrix}
```
## 2. Non-uniform basis functions
In order to achieve a curve where its first and last points would be at the same spots as its first and last control points respectively, we recursively calculate non-uniform basis functions using Cox-de Boor recursion formula.
```math
N_{i,0}(t)=\left\{
\begin{aligned}
1 \\
0
\end{aligned}
\;\middle|\
\begin{aligned}
\text{if }\; t_i \le t < t_{i+1} \\
otherwise
\end{aligned}
\right. 
```
```math
N_{i,j}(t)= \frac{t - t_i}{t_{i+j}-t_i}N_{i,j-1}(t) + \frac{t_{i+j+1} - t_i}{t_{i+j+1} - t_{i+1}}N_{i+1,j-1}(t)
```

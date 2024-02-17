# A non-iterated general implementation of the LPLS estimator for cOLS, TM, and custom cases

The program implements the **LPLS** (linear programming through least squares) estimator with the help of the Moore-Penrose inverse (pseudoinverse), calculated using *singular value decomposition (SVD)*, with emphasis on the estimation of OLS constrained in values (**cOLS**), Transaction Matrix (**TM**), and **custom** (user-defined) cases. The pseudoinverse offers a
unique minimum-norm least-squares solution, which is the best linear unbiased estimator (BLUE); see Albert (1972, Chapter VI). (Over)determined problems are accompanied by *regression* analysis, which is feasible in their case. For such and especially all remaining cases, a Monte Carlo-based
*ttest* of mean **NRMSE** (normalized by the standard deviation of the RHS) is performed, the sample being drawn from a uniform or user-provided distribution (via a *Python function*).

OLS constrained in values (**cOLS**) is an estimation based on constraints in the model and/or data but not in parameters. Typically, such models are of size ≤ **kN**, where **N** is the number of observations, since the number of their constraints may vary in the LHS (e.g., level, derivatives, etc.).

**Example of a cOLS problem:**  
*Estimate the trend and the cyclical component of a country's GDP given the textbook or any other definition of its peaks, troughs, and saddles. For a pre-LPLS approach to this problem, see (Bolotov, 2014).*

Transaction Matrix (**TM**) of size (**M x N**) is a formal model of interaction (allocation, assignment, etc.). between **M** and **N** elements in any imaginable system, such as intercompany transactions (netting tables), industries within/between economies (input-output tables), cross-border trade/investment (trade/investment matrices), etc., where **row** and **column sums** are known, but **individual elements** of the TM may not be:  

- a netting table is a type of **TM** where **M = N** and the elements are subsidiaries of a MNC;
- an input-output table (IOT) is a type of **TM** where **M = N** and the elements are industries;
- a matrix of trade/investment is a type of **TM** where **M = N** and the elements are countries or (macro)regions, where diagonal elements may be equal to zero;
- a country-product matrix is a type of **TM** where **M ≠ N** and the elements are of different types;  
...

**Example of a TM problem:**  
*Estimate the matrix of trade/investment with/without zero diagonal elements, the country shares in which are unknown. For a pre-LPLS approach to this problem, see (Bolotov, 2015).*

## Methods and formulas:
The LP problem in the **LPLS** estimator is a matrix equation **`a @ x = b`**, loosely based on the structure of the Simplex tableau, where **`a`** consists of coefficients for CONSTRAINTS, LP-type CHARACTERISTIC and/or SPECIFIC, and for SLACK/SURPLUS VARIABLES (the upper part) as well as for the MODEL (the lower part), as illustrated in Figure 1. Each part of **`a`** can be omitted to accommodate a particular case:  

- **cOLS** problems require SPECIFIC CONSTRAINTS, no LP-type CHARACTERISTIC CONSTRAINTS, and a MODEL;  
- **TM** requires LP-type CHARACTERISTIC CONSTRAINTS, no SPECIFIC CONSTRAINTS, and an optional MODEL;  
- SLACK/SURPLUS VARIABLES are included only for inequality constraints and should be set to **1** or **-1**;  
...

**Figure 1: Matrix equation `a @ x = b`**

| `a` || `b` |
| :-: |:-:| :-: |
| CONSTRAINTS: CHARACTERISTIC/SPECIFIC | SL/SU VARIABLES | CONSTRAINTS |
| MODEL || MODEL |

Source: self-prepared

The solution to the equation, **`x = pinv(a) @ b`**, is estimated with the help of SVD and is a **minimum-norm least-squares generalized solution** if the rank of **`a`** is not full. To check if **`a`** is within the computational limits, its (maximum) dimensions can be calculated using the formulas:  

- **(k \* N) x (K + K\*)** **cOLS** - without slack/surplus variables;
- **(k \* N) x (K + K\* + l)** **cOLS** - with slack/surplus variables;
- **(M + N) x (M \* N)** **TM** - without slack/surplus variables;
- **(M + N) x (M \* N + l**) **TM** - with slack/surplus variables;
- **M x N**  **custom** - without slack/surplus variables;
- **M x (N + l)** **custom** - with slack/surplus variables;

where, in **cOLS** problems, **K** is the number of independent variables in the model (including the constant), **K\*** is the number of eventual extra variables in CONSTRAINTS, and **N** is the number of observations; in **TM**, **M** and **N** are the dimensions of the matrix; and in **custom** cases, **M** and **N** or **M x (N + l)** are the dimensions of **`a`**.

## Parameters:
**Type of the LP problem**  

- `cols=False` : *bool*, OLS constrained in values (**cOLS**)  
- `tm=False` : *bool*, Transaction Matrix (**TM**), options **cols** and **tm** are mutually exclusive (not specifying any of them equals **custom**)  
- `rhs=np.empty((0,0))` : *array_like*, right-hand side of the problem (rowsums first for TM problems)

**Constructing the LHS**  

- `model=np.empty((0,0))` : *array_like*, the MODEL part of **`a`**, including an eventual user-provided constant as a matrix column in **cOLS** (see Methods and formulas)  
- `constraints=np.empty((0,0))` : *array_like*, the CONSTRAINTS part of **`a`**  
- `slackvars=np.empty((0,0))` : *array_like*, the SLACK/SURPLUS VARIABLES part of **`a`**  
- `zero_diagonal=False` : *bool*, set all the diagonal elements of **`a`** to 0  

**SVD-based estimation**  

- `tolerance=None` : *float*, scipy.linalg.lstsq's cutoff for `small' singular values; used to determine effective rank of a. Singular values smaller than cond \* largest_singular_value are considered zero
- `level=95` : *int*, confidence level (by default: **95**)

**Monte-Carlo-based t-test**  

- `seed=123456789` : *int*, random-number seed, # is any number between 0 and 2^31-1 (or 2,147,483,647) (by default: **123456789**) 
- `iterate=300` : *int*, number of iterations, # must be divisible by 50 (by default: **300**)  
- `distribution=runiform`: *fucntion*, random-variable generating function, name of an earlier declared Python object returning an *array_like* **(r x c)** with two arguments, real scalars **r** and **c** (by default: **lppinv.runiform**, see Examples on how to pass np.random.uniform to **lppinv**)  
- `mc=True` : *bool*, skip the Monte Carlo-based t-test  
- `trace=True`: *bool*, hide any output with the exception of dots

## Results:

**`class lppinv.LPpinvResult(`**  

- `OLSResults` : *statsmodels.regression.linear_model.OLSResults* or *None*, statsmodels' results class for for an OLS model  
- `TtestResult` : *(scipy.stats._result_classes.TtestResult, scipy.stats._result_classes.TtestResult, scipy.stats._result_classes.TtestResult)* or *(None, None, None)*, scipy's result of a t-test  
- `solution` : *array_like*, the solution obtained from the **LPLS** estimator  
- `a` : *array_like*, the **`a`** matrix  
- `nrmse` : *float*, root mean square error normalized by the standard deviation of **`b'**
- `r2_c` : *float* or *np.nan*, R-squared for CONSTRAINTS in TM  

**)**

## Errors:

- `LPpinvError` : *lppinv.LPpinvError*, specific Python-exception-derived object raised by lppinv functions  
- `LinAlgError` : *scipy.linalg.LinAlgError*, generic Python-exception-derived object raised by linalg functions  

## Examples:
```
import numpy  as np
import lppinv as lp

# cOLS problem
print('\n', lp.solve(
    cols=True,
    rhs=np.array([[0, 0, 0, 0, -1, 0.2, 0.9, 2.1]]).T,
    constraints=np.array([np.ones(4), [0, 1, 2, 3], [0, 5, 2, 8]]).T,
    model=np.array([np.ones(4), [0, 1, 2, 3], [0, 5, 2, 8]]).T,
    slackvars=np.array([[-1, 1, -1, 0]]).T,
    mc=False
))

# TM problem
def rnormal(r=None, c=None):
    return (np.random.normal(loc=0.0, scale=1.0, size=(r, c)))

print('\n', lp.solve(
    tm=True,
    rhs=np.array([[4, 5, 3, 4, 6], [1, 2, 0, np.nan, np.nan]]).T,
    zero_diagonal=True,
    distribution=rnormal
))

# custom problem
print('\n', lp.solve(
    rhs=np.array([[2, 3, 9], [5, 7, 9]]).T,
    model=np.vstack([[0, 1, 1], [1, 0, 1], [1, 1, 0]]),
    tolerance=10**-10,
    trace=False
))
```

## References:

1. Albert, A., 1972. *Regression And The Moore-Penrose Pseudoinverse.* New York: Academic Press.  

2. Bolotov, I. 2014. *Modeling of Time Series Cyclical Component on a Defined Set of Stationary Points and its Application on the US Business Cycle. [Paper presentation]. The 8th International Days of Statistics and Economics: Prague.* https://msed.vse.cz/msed_2014/article/348-Bolotov-Ilya-paper.pdf  

3. Bolotov, I. 2015. *Modeling Bilateral Flows in Economics by Means of Exact Mathematical Methods.* [Paper presentation]. The 9th International Days of Statistics and Economics: Prague. https://msed.vse.cz/msed_2015/article/111-Bolotov-Ilya-paper.pdf  

**PS** Please also check the Web of Science (WoS) for new research on LPLS.

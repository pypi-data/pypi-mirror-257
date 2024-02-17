import numpy           as     np
from   scipy.linalg    import lstsq
from   scipy.stats     import ttest_1samp
from   statsmodels.api import OLS

class LPpinvResult: # -------------------------------------------------------- #
    """result class  """
    def __init__(self, ols, ttest, x, a, nrmse, r2_c):
        self.OLSResults  = ols
        self.TtestResult = ttest
        self.solution    = x
        self.a           = a
        self.nrmse       = nrmse
        self.r2_c        = r2_c
    def __repr__(self):
        return('LPpinvResult('                                                 +
                    'OLSResults='        + str(self.OLSResults       ) + ', '  +
                    'TtestResult='       + str(self.TtestResult      ) + ', '  +
                    'solution=np.array(' + str(self.solution.tolist()) + '), ' +
                    'a=np.array('        + str(self.a.tolist()       ) + '), ' +
                    'nrmse='             + str(self.nrmse            ) + ', '  +
                    'r2_c='              + str(self.r2_c             ) + ')'   )

class LPpinvError(Exception): # ---------------------------------------------- #
    """error class   """
    pass

def runiform(
    # Function arguments (parameters) ---------------------------------------- #
    r=None, c=None
):
    """dummy function"""
    return (np.random.uniform(low=0.0, high=1.0, size=(r, c)))

def solve(
    # Function arguments (parameters) ---------------------------------------- #
    cols=False, tm=False, rhs=np.empty((0,0)), model=np.empty((0,0)),
    constraints=np.empty((0,0)), slackvars=np.empty((0,0)), zero_diagonal=False,
    tolerance=None, level=95, seed=123456789, iterate=300,
    distribution=runiform, mc=True, trace=True
):
    """main function """
    # general configuration -------------------------------------------------- #
    lp = 'cols' if cols else 'tm' if tm else 'custom'
    if cols and tm:
        raise LPpinvError('Arguments cols and tm are mutually incompatible')
    b  = np.array(rhs  )
    M  = np.array(model)
    C  = np.array(constraints)
    S  = np.array(slackvars)
    if level != int(level) or not (0 <= level <= 100):
        raise LPpinvError('The confidence level must lie between 0 and 99')

    # prepare LHS (left-hand side), `a`, and RHS (right-hand side), `b` ------ #
    if lp.lower() == 'cols':                           # LS-LP type: cOLS       
        if ((C.shape[0] + M.shape[0] > b.shape[0])):
            b = np.concatenate([b, b])
    if lp.lower() == 'tm':                             # LS-LP type: TM         
        if (not b.shape[0] or ((b.shape[0] > 1) and (b.shape[1] != 2))
                           or ((S.shape[0] > 1) and (S.shape[1] != 2))):
            raise LPpinvError('TM requires two columns in `b`')
        # C -> characteristic matrix                                            
        i = b.shape[0] - M.shape[0]
        r = np.sum(b[:i,0] < np.inf)                   # rows and cols          
        c = np.sum(b[:i,1] < np.inf)
        C = np.row_stack([
            np.kron(np.identity(r), np.ones(c)),       # rowsums (first)        
            np.kron(np.ones(r), np.identity(c)),       # colsums                
        ])
        # S -> characteristic matrix                                            
        if S.shape != (0,0):
            S =(lambda S: S[~np.isnan(S).any(axis=1)])(np.concatenate([
                S[:,0], S[:,1]
            ]).reshape((-1, 1)))
    # M, C, S -> `a` --------------------------------------------------------- #
    if zero_diagonal and lp.lower() == 'tm':           # diagonal of C -> M     
        M = np.row_stack([
            M if M.shape[0] else np.empty((0, r * c)),
            [np.kron(np.identity(min(r, c))[i], np.identity(max(r, c))[i])
             for i in range(min(r, c))]
        ])
    a = np.row_stack([
        np.column_stack([C, S if S.shape[0] else np.empty((C.shape[0], 0))])
        if C.shape[0]            else np.empty((0, M.shape[1] + S.shape[1])),
        np.column_stack([M, np.zeros((M.shape[0],  S.shape[1]))           ])
        if M.shape[0]            else np.empty((0, C.shape[1] + S.shape[1]))
    ])
    # `b` -> (-1, 1) --------------------------------------------------------- #
    if lp.lower() == 'tm':
        b = np.concatenate([b[:r,0], b[:c,1],
            np.sum(b[max(r, c):,:], axis=1) if b.shape[0] > max(r, c)
                                            else np.empty((0))
        ]).reshape((-1, 1))
    if zero_diagonal and lp.lower() == 'tm':           # diagonal of C -> b     
        b = np.row_stack([b, np.zeros((a.shape[0] - b.shape[0], 1))])
    # check dimensions of `a` and `b` ---------------------------------------- #
    if a.shape[0] != b.shape[0]:
        raise LPpinvError('`a` and `b` are not conformable')
    # drop missing values of `a` and `b` ------------------------------------- #
    a = a[~(np.isnan(a).any(axis=1) | np.isnan(b).any(axis=1))]
    b = b[~(np.isnan(a).any(axis=1) | np.isnan(b).any(axis=1))]
    C = M = C[~np.isnan(C).any(axis=1)].shape[0]       # clear memory           
    S =     S.shape[1]
    # check dimensions of `a` and `b` ---------------------------------------- #
    if a.shape[0] != b.shape[0]:
        raise LPpinvError('`a` and `b` are not conformable')

    # obtain the SVD-based solution of the matrix equation `a @ x = b` ------- #
    x, res, rank, s = lstsq(a, b, cond=tolerance)      # solution, NRMSE, R2_C  
    e = np.row_stack([
        (np.sqrt(np.sum((b - a @ x) ** 2) / (r := b.shape[0]) / np.var(b))),
        (1 - np.sum((b - a @ x)[:C] ** 2) / np.sum((b - b / C)[:C] ** 2) if C
         else np.nan)
    ])
    # regression results (if applicable) ------------------------------------- #
    ols   = None
    if lp.lower() != 'custom' and a.shape[1] <= b.shape[0]:
        ols = OLS(b, a).fit()
        print(ols.summary(alpha=round(1-level/100, 2)))
    # NRMSE t-test for `a', based on MC with iterate simulations ------------- #
    ttest = [None, None, None]
    if not np.isnan(e[0,0]) and mc:                    # skip if NRMSE == np.nan
        e = np.row_stack([
            e,
            (tmp := np.trunc(np.log10(iterate))) + np.trunc(tmp / 3) + 2
        ])                                             # format: %e[3].0fc      
        print('\nSimulations (\033[1m' + '{:.0f}'.format(iterate) + '\033[0m)')
        print('----+--- 1 ---+--- 2 ---+--- 3 ---+--- 4 ---+--- 5\n')
        np.random.seed(seed)
        for i in range(1, iterate + 1):
            e = np.row_stack([
                e,
                np.sqrt(np.sum(((b := distribution(r, 1))                     -
                                a @ lstsq(a, b, cond=tolerance)[0]) ** 2) / r /
                        np.var(b))
            ])
            if i %  5 == 0: print('.....', end='')
            if i % 50 == 0: print(('{:' + str(int(e[2,0])) + '.0f}').format(i))
        if trace:
            ttest[0]          = ttest_1samp(e[3:,0], popmean=e[0,0],
                                                  alternative='less'     )
            statistic, pvalue = ttest[0]
            ci_lb,     ci_ub  = ttest[0].confidence_interval(level / 100 )
            f = np.ceil(np.log10(abs(statistic))) + 6
            print('\n'  + 'One-sample t test'                            +
                  '\n'  + 'H0: mean      = \033[1m',
                  ('{:' + str(int(f)) + '.4f}').format(e[0,0]),
                                                                '\033[0m',
                  '  Mean:\033[1m                       '                +
                  ('{:' + str(int(f)) + '.4f}').format(np.mean(e[3:,0])) )
            print(        'Ha: mean      < \033[1m',
                  ('{:' + str(int(f)) + '.4f}').format(e[0,0]),
                                                                '\033[0m',
                  '  Std. dev.:\033[1m                  '                +
                  ('{:' + str(int(f)) + '.4f}').format(np.std(e[3:,0],
                                                                 ddof=1)))
            print(        'Pr(T < t)     = \033[1m',
                  ('{:' + str(int(f)) + '.4f}').format(pvalue), '\033[0m',
                  '  '  + str(level)  + '% conf. interval:\033[1m'       +
                  ('{:' + str(int(f)) + '.4f}').format(ci_lb) + ' '      +
                  ('{:' + str(int(f)) + '.4f}').format(ci_ub) + '\033[0m')
            ttest[1]          = ttest_1samp(e[3:,0], popmean=e[0,0],
                                                  alternative='two-sided')
            statistic, pvalue = ttest[1]
            ci_lb,     ci_ub  = ttest[1].confidence_interval(level / 100 )
            f = np.ceil(np.log10(abs(statistic))) + 6
            print('\n'  + 'H0: mean      = \033[1m',
                  ('{:' + str(int(f)) + '.4f}').format(e[0,0]),
                                                                '\033[0m',
                  '  Mean:\033[1m                       '                +
                  ('{:' + str(int(f)) + '.4f}').format(np.mean(e[3:,0])) )
            print(        'Ha: mean      !=\033[1m',
                  ('{:' + str(int(f)) + '.4f}').format(e[0,0]),
                                                                '\033[0m',
                  '  Std. dev.:\033[1m                  '                +
                  ('{:' + str(int(f)) + '.4f}').format(np.std(e[3:,0],
                                                                 ddof=1)))
            print(        'Pr(|T| > |t|) = \033[1m',
                  ('{:' + str(int(f)) + '.4f}').format(pvalue), '\033[0m',
                  '  '  + str(level)  + '% conf. interval:\033[1m'       +
                  ('{:' + str(int(f)) + '.4f}').format(ci_lb) + ' '      +
                  ('{:' + str(int(f)) + '.4f}').format(ci_ub) + '\033[0m')
            ttest[2]          = ttest_1samp(e[3:,0], popmean=e[0,0],
                                                  alternative='greater'  )
            statistic, pvalue = ttest[2]
            ci_lb,     ci_ub  = ttest[2].confidence_interval(level / 100 )
            f = np.ceil(np.log10(abs(statistic))) + 6
            print('\n'  + 'H0: mean      = \033[1m',
                  ('{:' + str(int(f)) + '.4f}').format(e[0,0]),
                                                                '\033[0m',
                  '  Mean:\033[1m                       '                +
                  ('{:' + str(int(f)) + '.4f}').format(np.mean(e[3:,0])) )
            print(        'Ha: mean      > \033[1m',
                  ('{:' + str(int(f)) + '.4f}').format(e[0,0]),
                                                                '\033[0m',
                  '  Std. dev.:\033[1m                  '                +
                  ('{:' + str(int(f)) + '.4f}').format(np.std(e[3:,0],
                                                                 ddof=1)))
            print(        'Pr(T > t)     = \033[1m',
                  ('{:' + str(int(f)) + '.4f}').format(pvalue), '\033[0m',
                  '  '  + str(level)  + '% conf. interval:\033[1m'       +
                  ('{:' + str(int(f)) + '.4f}').format(ci_lb) + ' '      +
                  ('{:' + str(int(f)) + '.4f}').format(ci_ub) + '\033[0m')

    # return the solution x, matrix a, and NRMSE ----------------------------- #
    return LPpinvResult(
        ols,
        tuple(ttest),
        (x[:x.shape[0]-S].reshape((-1, c)) if lp.lower() == 'tm'
                                           else x[:x.shape[0]-S]),
        a,
        e[0,0],
        (e[1,0] if e[1,0] >= 0
                else np.nan)
    )

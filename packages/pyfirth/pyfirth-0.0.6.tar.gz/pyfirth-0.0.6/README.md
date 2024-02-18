# pyfirth

The <code>pyfirth</code> package implements a very basic Firth-penalized logistic regression model for rare event data. There are likely more efficient and versatile methods out there.

## Dependencies

1) numpy
2) scipy
3) pandas
4) statsmodels

## Installation

The software package can be installed using pip by running the following command:
pip install pyfirth

##  Example

Here is a simple example made by binarizing some continuous data to create rare event data. Note, the Firth-penalized model is slightly more conservative.

``` python
    from pyfirth.PyFirth import PyFirth 
    import statsmodels.api as sm

    dta = sm.datasets.fair.load_pandas().data

    #create a rare count dataset by binning affair time into extreme not extreme
    dta["extreme_affairs"] = (dta["affairs"] > 20.0).astype(float)
    dta = sm.add_constant(dta)
    logit_mod = sm.Logit(dta["extreme_affairs"], dta[['const','occupation', 'educ', 'occupation_husb','rate_marriage','age','yrs_married','children','religious']])
    fitted_mod=logit_mod.fit()
    print('Logistic Regression Marriage Rating (Beta, SE, P): {0:.2f}, {1:.2f}, {2:.2e}'.format(fitted_mod.params['rate_marriage'],fitted_mod.bse['rate_marriage'],fitted_mod.pvalues['rate_marriage']))
    
    firth_test=PyFirth(dta,['const','occupation', 'educ', 'occupation_husb','rate_marriage','age','yrs_married','children','religious'],'extreme_affairs',hasconst=True)
    firth_output=firth_test.fit('rate_marriage')
    print('Firth Logistic Regression Marriage Rating (Beta, SE, P): {0:.2f}, {1:.2f}, {2:.2e}'.format(firth_output['ParamTable'].loc['rate_marriage']['BETA'],firth_output['ParamTable'].loc['rate_marriage']['SE'],firth_output['PVal']))

```

``` 
Optimization terminated successfully.
         Current function value: 0.037929
         Iterations 12
Logistic Regression Marri age Rating (Beta, SE, P): -0.79, 0.13, 3.85e-10
Firth Logistic Regression Marriage Rating (Beta, SE, P): -0.78, 0.12, 2.17e-09
```



You can also compare the results to the logistf package in R, which are quite similar. 
```python
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
import pandas as pd

with (ro.default_converter + pandas2ri.converter).context():
    r_dta = ro.conversion.get_conversion().py2rpy(dta)


r_firth_output = ro.r.logistf(formula='extreme_affairs ~ occupation+educ+occupation_husb+rate_marriage+age+yrs_married+children+religious',data=r_dta)
r_coeff=np.array(r_firth_output[0])
r_se = np.sqrt(np.array(r_firth_output[3]).diagonal())
r_pvalue = np.array(r_firth_output[20])

r_output_table = pd.DataFrame({'R_BETA':r_coeff,'R_SE':r_se,'R_PVAL':r_pvalue},index=['const','occupation', 'educ', 'occupation_husb','rate_marriage','age','yrs_married','children','religious'])
py_output_table = firth_output['ParamTable']
py_output_table['PVAL'] = pd.Series([firth_test.fit(covariate)['PVal'] for covariate in py_output_table.index],index=py_output_table.index)

print(r_output_table)
print(py_output_table)

```
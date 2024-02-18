import pandas as pd 
import numpy as np
from pyfirth.PyFirth import PyFirth

import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
importr('logistf')

design_matrix=pd.read_pickle('TestForFirth.pth')
firth_model=PyFirth(design_matrix,['Age', 'Gender','ObsTime', 'IsCaucasian','Genotype'],design_matrix.columns[-1],hasconst=False)
firth_output=firth_model.fit('Genotype',convergence_limit=1e-9)


with (ro.default_converter + pandas2ri.converter).context():
	r_dta = ro.conversion.get_conversion().py2rpy(design_matrix)
r_firth_output = ro.r.logistf(formula='{0:s} ~ Age+Gender+ObsTime+IsCaucasian+Genotype'.format(design_matrix.columns[-1]),data=r_dta)

r_coeff=np.array(r_firth_output[0])
r_se = np.sqrt(np.array(r_firth_output[3]).diagonal())
r_pvalue = np.array(r_firth_output[20])

r_output_table = pd.DataFrame({'R_BETA':r_coeff,'R_SE':r_se,'R_PVAL':r_pvalue},index=['const','occupation', 'educ', 'occupation_husb','rate_marriage','age','yrs_married','children','religious'])
py_output_table = firth_output['ParamTable']
py_output_table['PVAL'] = pd.Series([firth_test.fit(covariate)['PVal'] for covariate in py_output_table.index],index=py_output_table.index)

print(r_output_table)
print(py_output_table)
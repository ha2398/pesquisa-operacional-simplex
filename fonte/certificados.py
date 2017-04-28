"""
@author: Hugo Araujo de Sousa [2013007463]
"""

import simplex

def cert_inviabilidade(tableau):
	''' Retorna um certificado de inviabilidade de uma PL. Para isso, deve
		ser passado como parameto o tableau final da PL auxiliar dessa PL '''
	num_res = simplex.get_num_res(tableau)
	return tableau[0][0:num_res]
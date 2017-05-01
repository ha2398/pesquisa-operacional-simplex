"""
@author: Hugo Araujo de Sousa [2013007463]
"""

import simplex

def cert_inviabilidade(tableau_aux):
	''' Retorna um certificado de inviabilidade de uma PL. Para isso, deve
		ser passado como parameto o tableau final da PL auxiliar dessa PL '''
	return simplex.obtem_solucao_dual(tableau_aux)
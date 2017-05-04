"""
certificados.py: Define funções para obtenção de certificados de Programação
Linear.
@author: Hugo Araujo de Sousa [2013007463]
"""

import numpy as np
import simplex

def cert_inviabilidade(tableau_aux):
	''' Retorna um certificado de inviabilidade de uma PL. Para isso, deve
		ser passado como parameto o tableau final da PL auxiliar dessa PL,
		@tableau_aux.'''
	return simplex.obtem_solucao_dual(tableau_aux)

def cert_ilimitabilidade(tableau_final):
	''' Retorna um certificado de ilimitabilidade de uma PL. Para isso, deve
		ser passado como parameto o tableau final dessa PL, @tableau_final.'''
	num_res = simplex.get_num_res(tableau_final)
	num_colunas = len(tableau_final[0]) - 1

	# Procura pela coluna problemática no tableau.
	coluna_cert = num_res
	while (tableau_final[0][coluna_cert] >= 0):
		coluna_cert = coluna_cert + 1

	''' Constroi o certificado incrementalmente, passando por cada coluna do
		tableau. '''
	certificado = np.array([], dtype=float)
	for coluna in range(num_res, num_colunas):
		if (coluna == coluna_cert):
			certificado = np.append(certificado, 1)
			continue

		coluna_atual = tableau_final[0:num_res+1, coluna]

		if (simplex.checa_coluna_basica(coluna_atual)):
			#Procura pelo elemento == 1 na coluna.
			for linha in range(1, num_res+1):
				if (tableau_final[linha][coluna] == 1):
					certificado = np.append(certificado, -1 * \
						tableau_final[linha][coluna_cert])
					break
		else:
			certificado = np.append(certificado, 0)

	return certificado
"""
@author: Hugo Araujo de Sousa [2013007463]
"""

import numpy as np
import simplex

def ajusta_base_aux(original, auxiliar):
	''' Ajusta a base viavel da PL auxiliar '''

	num_res = simplex.get_num_res(original)
	num_var = simplex.get_num_var(original)

	for i in range(0, num_res):
		auxiliar = simplex.pivoteamento(auxiliar, i+1, num_var+i)

	return auxiliar

def constroi_auxiliar(pl):
	''' Constroi a PL auxiliar de uma PL a fim de verificar viabilidade '''
	num_res = simplex.get_num_res(pl)
	num_var = simplex.get_num_var(pl)

	auxiliar = simplex.FPI(pl)

	# Faz b >= 0
	for i in range(1, num_res+1):
		if (auxiliar[i][len(auxiliar[i])-1] < 0):
			auxiliar[i] = auxiliar[i] * -1

	# Constroi a primeira linha
	zeros = np.array([0 for i in range(0, num_var)], dtype=float)
	uns = np.array([-1 for i in range(0, num_res+1)], dtype=float)
	uns[-1] = 0.
	primeira_linha = np.concatenate((zeros,uns), axis=0)
	auxiliar[0] = primeira_linha

	# Ajusta a base viavel da PL
	auxiliar = ajusta_base_aux(pl, auxiliar)

	return auxiliar

def checa_viabilidade(pl):
	''' Checa a viabilidade de uma PL. Retorna True se a PL for viavel e False
		caso contrario. '''

	auxiliar = constroi_auxiliar(pl)
	tableau_f = simplex.simplex_primal(auxiliar)[0]
	otimo = simplex.val_obj_otimo_p(tableau_f)

	return (otimo == 0)
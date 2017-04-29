"""
@author: Hugo Araujo de Sousa [2013007463]
"""

import numpy as np
import simplex

def constroi_auxiliar(pl):
	''' Constroi o tableau auxiliar de uma PL, para verificar viabilidade '''
	auxiliar = simplex.tableau_inicial(simplex.FPI(pl))

	num_res = simplex.get_num_res(auxiliar)
	num_var = simplex.get_num_var(auxiliar)

	# Faz b >= 0
	for i in range(1, num_res+1):
		if (auxiliar[i][len(auxiliar[i])-1] < 0):
			auxiliar[i] = auxiliar[i] * -1

	# Constroi a primeira linha
	zeros = np.array([0 for i in range(0, num_var)], dtype=float)
	uns = np.array([1 for i in range(0, num_res+1)], dtype=float)
	uns[-1] = 0.
	primeira_linha = np.concatenate((zeros,uns), axis=0)

	# Adiciona identidade a matriz A.
	zero_fill = np.array([0 for i in range(0, num_res)], dtype=float)
	identidade = np.transpose(np.insert(np.identity(num_res), 0, zero_fill, axis=0))
	for i in range(num_res-1, -1, -1):
		auxiliar = np.insert(auxiliar, num_var, identidade[i], axis=1)

	# Adiciona a primeira linha auxiliar criada.
	auxiliar[0] = primeira_linha

	# Ajusta a base viavel da PL
	base_viavel = list(range(len(zeros), len(zeros)+len(uns)-1))	

	return (auxiliar, base_viavel)

def checa_viabilidade(pl):
	''' Checa a viabilidade de uma PL. Retorna True se a PL for viavel e False
		caso contrario. '''

	auxiliar, base = constroi_auxiliar(pl)
	tableau_f = simplex.simplex_primal(auxiliar, base)[0]
	otimo = simplex.val_obj_otimo_p(tableau_f)

	return ((otimo == 0), tableau_f)

def obtem_base_viavel(tableau_aux):
	''' Retorna uma lista que contem o indice das colunas que formam uma base
		viavel para a PL que gera o tableau auxiliar tableau_aux '''
	base = []
	solucao_aux = simplex.obtem_solucao(tableau_aux)
	num_res = simplex.get_num_res(tableau_aux)
	tam_solucao = len(solucao_aux)

	# Captura os indices das variaveis nao nulas na solucao da PL auxiliar.
	for i in range(0, tam_solucao):
		if (solucao_aux[i] != 0):
			base.append(i)

	return base
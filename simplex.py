"""
@author: Hugo Araujo de Sousa [2013007463]
"""

NOME_SAIDA = "output.txt"

import numpy as np
import simplex_io as sio

def get_num_res(matriz):
	''' Retorna o numero de restricoes da PL '''
	return len(matriz) - 1

def get_num_var(matriz):
	''' Retorna o numero de variaveis da PL '''
	return len(matriz[0]) - 1

def matriz_id(num_res):
	''' Cria matriz identidade a ser adicionada ao primeiro tableau '''
	zeros = [[0. for x in range(0, num_res)]]
	identidade = np.identity(num_res)
	identidade = np.append(zeros, identidade, axis = 0)
	return identidade

def tableau_inicial(matriz):
	''' Merge uma matriz e a identidade para obter o primeiro tableau '''
	num_var = get_num_var(matriz)
	num_res = get_num_res(matriz)

	identidade_t = np.transpose(matriz_id(num_res))

	nova_matriz = matriz

	for i in range(num_res-1, -1, -1):
		nova_matriz = np.insert(nova_matriz, num_var, identidade_t[i], axis=1)

	for i in range(num_res-1, -1, -1):
		nova_matriz = np.insert(nova_matriz, 0, identidade_t[i], axis=1)

	nova_matriz[0] = nova_matriz[0] * -1
	return nova_matriz

def simplex_primal_continua(tableau):
	''' Retorna true se e somente se o simplex primal ainda tem iteracoes a
		executar '''
	primeira_linha = tableau[0]
	num_neg = [neg for neg in primeira_linha if neg < 0]
	return len(num_neg) > 0

def simplex_primal(matriz): #TODO
	''' Aplica a o simplex primal a uma matriz '''
	arquivo_saida = open(NOME_SAIDA, 'w')

	num_var = get_num_res(matriz)
	identidade = matriz_id(num_var)

	tableau = tableau_inicial(matriz)
	sio.imprime_matriz(tableau, arquivo_saida)

	print tableau

	arquivo_saida.close()
"""
@author: Hugo Araujo de Sousa [2013007463]
"""

import numpy as np
import simplex_auxiliar as aux
import simplex_io as sio

def get_num_res(pl):
	''' Retorna o numero de restricoes da PL '''
	return len(pl) - 1

def get_num_var(pl):
	''' Retorna o numero de variaveis da PL '''
	return len(pl[0]) - 1

def matriz_id(num_res):
	''' Cria matriz identidade a ser adicionada ao primeiro tableau '''
	zeros = [[0. for x in range(0, num_res)]]
	identidade = np.identity(num_res)
	identidade = np.append(zeros, identidade, axis = 0)
	return identidade

def FPI(pl):
	''' Coloca uma PL em forma padrao de igualdades '''

	fpi = np.copy(pl)
	num_var = get_num_var(pl)
	num_res = get_num_res(pl)

	identidade_t = np.transpose(matriz_id(num_res))

	for i in range(num_res-1, -1, -1):
		fpi = np.insert(fpi, num_var, identidade_t[i], axis=1)

	return fpi

def tableau_inicial(pl):
	''' Merge uma PL em FPI e a identidade para obter o primeiro tableau '''

	num_res = get_num_res(pl)
	nova_matriz = FPI(pl)
	identidade_t = np.transpose(matriz_id(num_res))

	for i in range(num_res-1, -1, -1):
		nova_matriz = np.insert(nova_matriz, 0, identidade_t[i], axis=1)

	colunas = len(nova_matriz[0])

	# Multiplica a primeira linha por -1
	for i in range(0, colunas):
		if (nova_matriz[0][i] != 0):
			nova_matriz[0][i] = nova_matriz[0][i] * -1

	return nova_matriz

def simplex_primal_continua(tableau, num_res):
	''' Retorna True se e somente se o simplex primal ainda tem iteracoes a
		executar '''
	primeira_linha = tableau[0][num_res:len(tableau[0])-1]
	num_neg = [neg for neg in primeira_linha if neg < 0]

	return len(num_neg) > 0

def escolhe_pivot_p(tableau, num_res):
	''' Retorna o indice do elemento pivot no tableau atual, considerando
		o metodo de simplex primal '''
	primeira_linha = tableau[0][num_res:len(tableau[0])-1]
	coluna = num_res

	while (primeira_linha[coluna] > 0):
		coluna = coluna + 1

	razoes = []
	num_linhas_tableau = len(tableau)
	num_colunas_tableau = len(tableau[0])

	# Obtem as razoes nao-negativas
	for i in range(num_linhas_tableau-1, 0, -1):
		a = tableau[i][coluna]

		if (a == 0):
			continue

		b = tableau[i][num_colunas_tableau-1]
		razao = b/a

		if razao > 0:
			razoes.insert(0, (razao, i))

	# Checa se nao ha razoes nao-negativas
	if (len(razoes) == 0):
		return (-1, -1)

	razoes = sorted(razoes, key=lambda tup: tup[0])
	return (razoes[0][1], coluna)

def pivoteamento(tableau, i, j):
	''' Realiza o pivoteamento em um tableau, tendo como elemento pivot
		o elemento dado pelos indices i e j, ou seja T[i][j] '''
	colunas = len(tableau[0])
	linhas = len(tableau)
	pivot = tableau[i][j]

	if (pivot != 1):
		for k in range(0, colunas):
			tableau[i][k] = tableau[i][k] / pivot

		pivot = tableau[i][j]

	# Para cada linha do tableau
	for k in range(0, linhas):
		if (k == i):
			continue

		# Pivotea cada elemento da linha
		fator = -1 * tableau[k][j]
		for x in range(0, colunas):
			tableau[k][x] = (tableau[i][x] * fator) + tableau[k][x]

	return tableau

def val_obj_otimo_p(tableau):
	''' Retorna o valor objetivo da PL de acordo com o tableau passado como
		parametro. '''
	return tableau[0][len(tableau[0])-1]

def checa_coluna_basica(coluna):
	''' Retorna True se, e somente se, a coluna eh basica no tableau '''
	basica = False
	num_zeros = 0
	num_uns = 0
	tam_coluna = len(coluna)

	for i in range(0, tam_coluna):
		if (coluna[i] == 0):
			num_zeros = num_zeros + 1
		elif (coluna[i] == 1):
			num_uns = num_uns + 1

	if (num_zeros == (tam_coluna-1) and num_uns == 1):
		basica = True

	return basica

def obtem_solucao(tableau, num_res):
	''' Retorna o vetor que representa a solução da PL representada pelo
		tableau final passado com parametro.'''
	solucao = np.array([], dtype=float)
	num_linhas = len(tableau)
	num_colunas = len(tableau[0])
	b = tableau[0:num_linhas+1, num_colunas-1]

	# Analisa cada coluna
	for i in range(num_res, num_colunas):
		coluna_atual = tableau[0:num_linhas+1, i]

		if (checa_coluna_basica(coluna_atual)):
			for j in range(1, num_linhas):
				if (coluna_atual[j] == 1):
					solucao = np.append(solucao, np.array(b[j]))
					break

	return solucao

def simplex_primal(pl):
	''' Aplica a o simplex primal a uma pl '''
	num_res = get_num_res(pl)
	identidade = matriz_id(num_res)
	saida = ""

	tableau = tableau_inicial(FPI(pl))

	saida = saida + sio.imprime_matriz(tableau)
	while (simplex_primal_continua(tableau, num_res)):
		i_pivot = escolhe_pivot_p(tableau, num_res)
		tableau = pivoteamento(tableau, i_pivot[0], i_pivot[1])
		saida = saida + sio.imprime_matriz(tableau)

	return (tableau, saida)

def simplex_dual(pl):#TODO
	''' Aplica o simplex dual a uma pl '''

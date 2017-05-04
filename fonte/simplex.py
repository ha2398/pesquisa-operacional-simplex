"""
simplex.py: Define as funções para implementação do algoritmo Simplex.
@author: Hugo Araujo de Sousa [2013007463]
"""

import numpy as np
import simplex_auxiliar as aux
import simplex_io as sio

''' Precisão decimal considerada durantes os cálculos com números de
	ponto-flutuante.'''
PRECISAO_CALCULO = 10

def get_num_res(pl):
	''' Retorna o numero de restricoes da @pl '''
	return len(pl) - 1

def get_num_var(pl):
	''' Retorna o numero de variaveis da @pl '''
	return len(pl[0]) - 1

def matriz_op(num_res):
	''' Cria matriz de operacoes a ser adicionada ao primeiro tableau. @num_res
		representa o número de restrições da PL.'''
	zeros = [[0. for x in range(0, num_res)]]
	op = np.identity(num_res)
	op = np.append(zeros, op, axis = 0)
	return op

def FPI(pl):
	''' Coloca uma @pl em forma padrao de igualdades '''
	fpi = np.copy(pl)
	num_var = get_num_var(pl)
	num_res = get_num_res(pl)

	identidade_t = np.transpose(matriz_op(num_res))

	for i in range(num_res-1, -1, -1):
		fpi = np.insert(fpi, num_var, identidade_t[i], axis=1)

	return fpi

def tableau_inicial(pl, modo):
	''' Merge uma @pl em FPI e a identidade para obter o primeiro tableau. 
		@modo indica o modo de simplex que sera aplicado ao tableau.
		1 = Primal, 2 = Dual. '''
	num_res = get_num_res(pl)
	tableau = np.copy(pl)

	identidade_t = np.transpose(matriz_op(num_res))

	for i in range(num_res-1, -1, -1):
		tableau = np.insert(tableau, 0, identidade_t[i], axis=1)

	colunas = len(tableau[0])

	# Multiplica a primeira linha por -1
	for i in range(0, colunas):
		if (tableau[0][i] != 0):
			tableau[0][i] = tableau[0][i] * -1

	# Garante que b >= 0 para simplex primal
	if (modo == 1):
		for i in range(1, num_res+1):
			if (tableau[i][colunas-1] < 0):
				tableau[i] = tableau[i] * -1

	return tableau

def simplex_primal_continua(tableau):
	''' Retorna True se e somente se o simplex primal ainda tem iteracoes a
		executar, considerando o @tableau passado como parametro.'''
	num_res = get_num_res(tableau)
	primeira_linha = tableau[0][num_res:len(tableau[0])-1]
	num_neg = [neg for neg in primeira_linha if neg < 0]

	return len(num_neg) > 0

def simplex_dual_continua(tableau):
	''' Retorna True se e somente se o simplex dual ainda tem iteracoes a
		executar, considerando o @tableau passado como parametro.'''
	num_res = get_num_res(tableau)
	b = tableau[1:num_res+1, len(tableau[0])-1]
	num_neg = [neg for neg in b if neg < 0]

	return len(num_neg) > 0

def escolhe_pivot_p(tableau):
	''' Retorna o indice do elemento pivot no @tableau atual, considerando
		o metodo de simplex primal.'''
	num_res = get_num_res(tableau)
	primeira_linha = tableau[0][num_res:len(tableau[0])-1]
	coluna = num_res

	while (primeira_linha[coluna-num_res] >= 0):
		coluna = coluna + 1

	razoes = []
	num_linhas_tableau = len(tableau)
	num_colunas_tableau = len(tableau[0])

	# Obtem as razoes nao-negativas
	for i in range(1, num_linhas_tableau):
		a = tableau[i][coluna]
		b = tableau[i][num_colunas_tableau-1]

		if (a == 0 or b == -0):
			continue

		razao = b/a

		if (razao >= 0):
			razoes.insert(0, (razao, i))

	# Checa se nao ha razoes nao-negativas
	if (len(razoes) == 0):
		return (-1, -1)

	razoes = sorted(razoes, key=lambda tup: tup[0])
	return (razoes[0][1], coluna)

def escolhe_pivot_d(tableau):
	''' Retorna o indice do elemento pivot no @tableau atual, considerando
		o metodo de simplex dual.'''
	num_res = get_num_res(tableau)
	b = tableau[1:num_res+1, len(tableau[0]) - 1]
	linha = 1

	while (b[linha-1] >= 0):
		linha = linha + 1

	razoes = []
	num_colunas_tableau = len(tableau[0])

	# Obtem as razoes nao-negativas
	for coluna in range(num_res, num_colunas_tableau-1):
		c = tableau[0][coluna]
		a = tableau[linha][coluna]

		# c deve ser maior ou igual a zero.
		# a deve ser negativo.
		if (c < 0 or a >= 0):
			continue
		
		razao = c / (-a)
		razoes.insert(0, (razao, coluna))

	# Checa se alguma razao valida foi encontrada.
	if (len(razoes) == 0):
		return (-1, -1)

	razoes = sorted(razoes, key=lambda tup: tup[0])
	return (linha, razoes[0][1])

def pivoteamento(tableau, i, j):
	''' Realiza o pivoteamento em um @tableau, tendo como elemento pivot
		o elemento dado pelos indices @i e @j, ou seja T[i][j] '''
	colunas = len(tableau[0])
	linhas = len(tableau)
	pivot = tableau[i][j]

	# Divide todos os elementos da linha por pivot
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

def ajusta_base(tableau, base):
	''' Ajusta a @base viavel de um @tableau.'''
	num_res = get_num_res(tableau)
	num_var = get_num_var(tableau) - num_res

	tam_base = len(base)
	novo_tableau = np.copy(tableau)

	for i in range(0, tam_base):
		novo_tableau = pivoteamento(novo_tableau, i+1, base[i])

	return novo_tableau

def val_obj_otimo_p(tableau):
	''' Retorna o valor objetivo da PL de acordo com o @tableau primal passado
		como parametro.'''
	return tableau[0][len(tableau[0])-1]

def val_obj_otimo_d(tableau):
	''' Retorna o valor objetivo da PL de acordo com o @tableau dual passado
		como parametro.'''
	return -1 * val_obj_otimo_p(tableau)

def checa_coluna_basica(coluna):
	''' Retorna True se, e somente se, a @coluna é básica no tableau.'''
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

def obtem_solucao(tableau):
	''' Retorna o vetor que representa a solucao da PL representada pelo
		@tableau final passado como parametro.'''
	solucao = np.array([], dtype=float)
	num_res = get_num_res(tableau)
	num_linhas = len(tableau)
	num_colunas = len(tableau[0]) - 1
	b = tableau[0:num_linhas+1, num_colunas]

	# Analisa cada coluna
	for i in range(num_res, num_colunas):
		coluna_atual = tableau[0:num_linhas+1, i]

		# Para colunas básicas:
		if (checa_coluna_basica(coluna_atual)):
			for j in range(1, num_linhas):
				if (coluna_atual[j] == 1):
					solucao = np.append(solucao, np.array(b[j]))
					break
		# Para colunas não-básicas:
		else:
			solucao = np.append(solucao, 0.0)

	return solucao

def obtem_solucao_dual(tableau):
	''' Retorna o vetor que representa a solucao da dual da PL representada
		pelo @tableau final passado como parametro. '''
	num_res = get_num_res(tableau)
	return tableau[0][0:num_res]

def simplex_primal(tableau, base):
	''' Aplica a o simplex primal a uma pl, tendo como ponto de partida 
		a @base viavel de colunas passada como parametro e o @tableau inicial.
		Retorna uma tupla que contem o tableau final e uma string que
		representa a sequencia de tableaux obtida durante o simplex '''
	num_res = get_num_res(tableau)
	identidade = matriz_op(num_res)
	saida = ""
	ilimitabilidade = False

	novo_tableau = ajusta_base(tableau, base)
	novo_tableau = np.around(novo_tableau, decimals=PRECISAO_CALCULO)
	saida = saida + sio.imprime_array(novo_tableau) + '\n'

	# Melhora a solucao indo de solucao basica viavel a solucao basica viavel.
	while (simplex_primal_continua(novo_tableau)):
		i_pivot = escolhe_pivot_p(novo_tableau)

		# Algoritmo encontra situacao de ilimitabilidade.
		if (i_pivot[0] < 0):
			ilimitabilidade = True
			break

		novo_tableau = pivoteamento(novo_tableau, i_pivot[0], i_pivot[1])
		novo_tableau = np.around(novo_tableau, decimals=PRECISAO_CALCULO)
		saida = saida + sio.imprime_array(novo_tableau) + '\n'

	return (novo_tableau, saida, ilimitabilidade)

def simplex_dual(tableau, base):
	''' Aplica a o simplex dual a uma pl, tendo como ponto de partida 
		a @base viavel de colunas passada como parametro e o @tableau inicial.
		Retorna uma tupla que contem o tableau final e uma string que
		representa a sequencia de tableaux obtida durante o simplex '''
	num_res = get_num_res(tableau)
	identidade = matriz_op(num_res)
	saida = ""
	ilimitabilidade = False

	novo_tableau = ajusta_base(tableau, base)
	novo_tableau = np.around(novo_tableau, decimals=PRECISAO_CALCULO)
	saida = saida + sio.imprime_array(novo_tableau) + '\n'

	# Melhora a solucao indo de solucao basica viavel a solucao basica viavel.
	while (simplex_dual_continua(novo_tableau)):
		i_pivot = escolhe_pivot_d(novo_tableau)

		novo_tableau = pivoteamento(novo_tableau, i_pivot[0], i_pivot[1])
		novo_tableau = np.around(novo_tableau, decimals=PRECISAO_CALCULO)
		saida = saida + sio.imprime_array(novo_tableau) + '\n'

	return (novo_tableau, saida, ilimitabilidade)

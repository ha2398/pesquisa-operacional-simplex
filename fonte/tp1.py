"""
@author: Hugo Araujo de Sousa [2013007463]
"""

import certificados as cert
import numpy as np
import simplex_auxiliar as aux
import simplex_io as sio
import simplex
import sys

def processa_entrada(nome_entrada):
	''' Abre o arquivo de entrada contendo a PL a ser resolvida '''

	return sio.le_matriz_entrada(nome_entrada)

def modo_execucao_1(pl):
	''' Modo de execucao 1 '''
	otimalidade, tableau_aux = aux.checa_viabilidade(pl)
	num_var = simplex.get_num_var(pl)

	# Para PLs viaveis:
	if (otimalidade == True):
		base = aux.obtem_base_viavel(tableau_aux)
		tableau_inicial = simplex.tableau_inicial(simplex.FPI(pl), 1)
		tableau_final, seq_tableaux, ilimitabilidade = \
			simplex.simplex_primal(tableau_inicial, base)

		# PLs ilimitadas.
		if (ilimitabilidade == True):
			cert_ilim = cert.cert_ilimitabilidade(tableau_final)
			cert_ilim = sio.imprime_array(cert_ilim)

			return "PL ilimitada, aqui está um certificado " + cert_ilim + "\n"
		# PLs limitadas.
		else:
			x = simplex.obtem_solucao(tableau_final)[0:num_var]
			x = sio.imprime_array(x)

			cTx = str(simplex.val_obj_otimo_p(tableau_final))

			y = simplex.obtem_solucao_dual(tableau_final)
			y = sio.imprime_array(y)

			return "Solução ótima x = " + x + ", com valor objetivo " + \
				cTx + ", e solução dual y = " + y + "\n"
	# Pls inviáveis.
	else:
		cert_inv = cert.cert_inviabilidade(tableau_aux)
		cert_inv = sio.imprime_array(cert_inv)
		return "PL inviável, aqui está um certificado " + cert_inv + "\n"

def modo_execucao_2(pl, tipo_simplex):
	''' Modo de execucao 2 '''

	# Checa tipo valido
	if (tipo_simplex < 1 or tipo_simplex > 2):
		print("[Erro]: Tipo de simplex invalido.")
		exit()

	num_var = simplex.get_num_var(pl)
	num_res = simplex.get_num_res(pl)

	base = [(i+num_res+num_var) for i in range(0, num_res)]

	# Simplex Primal
	if (tipo_simplex == 1):
		tableau_inicial = simplex.tableau_inicial(simplex.FPI(pl), tipo_simplex)
		return simplex.simplex_primal(tableau_inicial, base)[1]

	# Simplex Dual
	if (tipo_simplex == 2):
		tableau_inicial = simplex.tableau_inicial(simplex.FPI(pl), tipo_simplex)
		return simplex.simplex_dual(tableau_inicial, base)[1]


def main():
	''' Programa principal '''
	# Checa numero de argumentos recebidos
	if (len(sys.argv) != 3):
		print("[Erro]: Numero incorreto de parametros.")
		print("Uso: python", sys.argv[0], "<entrada> <saida>")
		return

	nome_entrada = sys.argv[1]
	nome_saida = sys.argv[2]

	# Processa o arquivo de entrada com a PL a ser resolvida
	pl, modo_execucao, tipo_simplex = processa_entrada(nome_entrada)

	# Checa opcao valida
	if (modo_execucao < 1 or modo_execucao > 2):
		print("[Erro]: Modo de execucao invalido.")
		exit()

	arquivo_saida = open(nome_saida, 'w')

	# Executa o programa de acordo com o modo selecionado
	if (modo_execucao == 1):
		saida = modo_execucao_1(pl)
	if (modo_execucao == 2):
		saida = modo_execucao_2(pl, tipo_simplex)

	print(saida, end="", file=arquivo_saida)
	arquivo_saida.close()

# Execucao do programa principal
sio.configura_impressao_float()
main()
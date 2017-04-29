"""
@author: Hugo Araujo de Sousa [2013007463]
"""

import certificados as cert
import numpy as np
import simplex_auxiliar as aux
import simplex_io as sio
import simplex
import sys

def menu():
	''' Exibe uma mensagem inicial com opcoes e retorna a opcao escolhida '''

	print("\tTrabalho Pratico 1")
	print("\tSIMPLEX\n")
	print("* Selecione o modo de execucao:\n")
	print("(1) PLs arbitrarias e grandes")
	print("(2) PL viavel e limitada\n")

	opcao = input("Modo: ")
	return opcao

def processa_entrada(nome_entrada):
	''' Abre o arquivo de entrada contendo a PL a ser resolvida '''

	return sio.le_matriz_entrada(nome_entrada)

def modo_execucao_1(pl): #TODO
	''' Modo de execucao 1 '''
	otimalidade, tableau_aux = aux.checa_viabilidade(pl)

	# Para PLs viaveis:
	if (otimalidade == True):
		base = aux.obtem_base_viavel(tableau_aux)
		tableau_inicial = simplex.tableau_inicial(simplex.FPI(pl))
		tableau_final, seq_tableaux, ilimitabilidade = \
			simplex.simplex_primal(tableau_inicial, base)

		if (ilimitabilidade == True):
			return "PL ilimitada\n"
		else:
			return "PL viavel\n"
	else:
		cert_inv = cert.cert_inviabilidade(tableau_aux)
		cert_str = np.array_str(cert_inv).replace('[', '{').replace(']', '}')
		return "PL inviável, aqui está um certificado " + cert_str + "\n"

def modo_execucao_2(pl): #TODO
	''' Modo de execucao 2 '''

	print("\n* Selecione o tipo de simplex:\n")
	print("(1) Primal")
	print("(2) Dual\n")

	tipo_simplex = int(input("Tipo: "))
	# Checa tipo valido
	if (tipo_simplex < 1 or tipo_simplex > 2):
		print("[Erro]: Tipo de simplex invalido.")
		exit()

	# Simplex Primal
	if (tipo_simplex == 1):
		tableau_inicial = simplex.tableau_inicial(simplex.FPI(pl))
		return simplex.simplex_primal(tableau_inicial, [4,5])[1]


def main():
	''' Programa principal '''
	# Checa numero de argumentos recebidos
	if (len(sys.argv) != 3):
		print("[Erro]: Numero incorreto de parametros.")
		print("Uso: python", sys.argv[0], "<entrada> <saida>")

	nome_entrada = sys.argv[1]
	nome_saida = sys.argv[2]

	modo_execucao = int(menu())
	# Checa opcao valida
	if (modo_execucao < 1 or modo_execucao > 2):
		print("[Erro]: Modo de execucao invalido.")
		exit()

	# Processa o arquivo de entrada com a PL a ser resolvida
	pl = processa_entrada(nome_entrada)

	arquivo_saida = open(nome_saida, 'w')

	# Executa o programa de acordo com o modo selecionado
	if (modo_execucao == 1):
		saida = modo_execucao_1(pl)
	if (modo_execucao == 2):
		saida = modo_execucao_2(pl)

	print(saida, end="", file=arquivo_saida)
	arquivo_saida.close()

# Execucao do programa principal
sio.configura_impressao_float()
main()
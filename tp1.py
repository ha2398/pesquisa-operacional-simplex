"""
@author: Hugo Araujo de Sousa [2013007463]
"""

import simplex_io as sio
import simplex

def menu():
	''' Exibe uma mensagem inicial com opcoes e retorna a opcao escolhida '''

	print("\tTrabalho Pratico 1")
	print("\tSIMPLEX\n")
	print("* Selecione o modo de execucao:\n")
	print("(1) PLs arbitrarias e grandes")
	print("(2) PL viavel e limitada\n")

	opcao = input("Modo: ")
	return opcao

def processa_entrada():
	''' Abre o arquivo de entrada contendo a PL a ser resolvida '''

	nome_entrada = input("Nome do arquivo de entrada (entre aspas): ")
	return sio.le_matriz_entrada(nome_entrada)

def modo_execucao_1(matriz): #TODO
	''' Modo de execucao 1 '''

def modo_execucao_2(matriz): #TODO
	''' Modo de execucao 2 '''

	print("\n* Selecione o tipo de simplex:\n")
	print("(1) Primal")
	print("(2) Dual\n")

	tipo_simplex = input("Tipo: ")
	# Checa tipo valido
	if (tipo_simplex < 1 or tipo_simplex > 2):
		print("[Erro]: Tipo de simplex_ioplex invalido.")
		exit()

	# Simplex Primal
	if (tipo_simplex == 1):
		simplex.simplex_primal(matriz)


def main():
	''' Programa principal '''

	modo_execucao = menu()
	# Checa opcao valida
	if (modo_execucao < 1 or modo_execucao > 2):
		print("[Erro]: Modo de execucao invalido.")
		exit()

	# Processa o arquivo de entrada com a PL a ser resolvida
	matriz_entrada = processa_entrada()

	# Executa o programa de acordo com o modo selecionado
	if (modo_execucao == 1):
		modo_execucao_1(matriz_entrada)
	if (modo_execucao == 2):
		modo_execucao_2(matriz_entrada)

# Execucao do programa principal
main()
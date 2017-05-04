"""
simplex_io.py: Define formato e funções de entrada e saída do algoritmo
Simplex implementado.
@author: Hugo Araujo de Sousa [2013007463]
"""

import ast
import numpy as np
import re

''' Define a precisão decimal com que os números de ponto-flutuante serão
    impressos. '''
PRECISAO_IMPRESSAO = 5

def configura_impressao_float():
    ''' Configura como os dados do tipo float em arrays numpy serao
        impressos.'''
    np.set_printoptions(precision=PRECISAO_IMPRESSAO, suppress=True)
    
def le_matriz_entrada(nome_entrada):
    ''' Le o arquivo de entrada de nome @nome_entrada e o transforma em uma
        matriz Numpy.'''
    arquivo_entrada = open(nome_entrada, 'r')
    entrada = arquivo_entrada.read().split()

    # Checa formato invalido de entrada.
    if (len(entrada) < 5):
        print("[Erro]: Arquivo de entrada inválido.")
        exit()

    # Modo de execucao
    modo_execucao = int(entrada[1])

    # Tipo de Simplex
    if (modo_execucao == 2):
        if(entrada[2] == 'P'):
            simplex = 1
        else:
            simplex = 2
    else:
        simplex = 0 # Nao especificado.

    # String que representa a PL.
    if (modo_execucao == 1):
        string_matriz = entrada[4]
    else:
        string_matriz = entrada[5]
    
    # Converte a string para o formato de input para Numpy
    string_matriz = string_matriz.replace("}", "]")
    string_matriz = string_matriz.replace("{", "[")

    matriz = np.array(ast.literal_eval(string_matriz), dtype=float)
    
    arquivo_entrada.close()
    return (matriz, modo_execucao, simplex) 

def imprime_array(array):
    ''' Converte um @array numpy para uma string no formato definido pelo
        problema.'''
    string = np.array_str(array)
    string = re.sub(' +', ' ', string)

    string = string.replace("[ ", "[")
    string = string.replace(" ]", "]")
    string = string.replace("[", "{")
    string = string.replace("]", "}")
    string = string.replace("\n ", ",")
    string = string.replace(" ", ",")

    # Remove ponto flutuante de numeros com parte decimal = 0.
    string = string.replace(".,", ",")
    string = string.replace(".}", "}")

    # Adiciona quebra de linha ao final da string
    string = string

    return string
"""
@author: Hugo Araujo de Sousa [2013007463]
"""

import ast
import numpy as np
import re

PRECISAO_IMPRESSAO = 3

def configura_impressao_float():
    ''' Configura como os dados do tipo float em arrays numpy serao
        impressos '''
    np.set_printoptions(precision=PRECISAO_IMPRESSAO)
    
def le_matriz_entrada(nome_entrada):
    ''' Le o arquivo de entrada e o transforma em uma matriz Numpy '''

    arquivo_entrada = open(nome_entrada, 'r')
    string_matriz = arquivo_entrada.read()
    
    # Converte a string para o formato de input para Numpy
    string_matriz = string_matriz.replace("}", "]")
    string_matriz = string_matriz.replace("{", "[")

    matriz = np.array(ast.literal_eval(string_matriz), dtype=float)
    
    arquivo_entrada.close()
    return matriz

def imprime_array(array):
    ''' Converte um array numpy para uma string no formato definido pelo
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
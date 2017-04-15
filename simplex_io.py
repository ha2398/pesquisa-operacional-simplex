"""
@author: Hugo Araujo de Sousa [2013007463]
"""

import ast
import numpy as np
import re

def le_matriz_entrada(nome_entrada):
    ''' Le o arquivo de entrada e o transforma em uma matriz Numpy '''

    arquivo_entrada = open(nome_entrada, 'r')
    string_matriz = arquivo_entrada.read()
    
    # Converte a string para o formato de input para Numpy
    string_matriz = string_matriz.replace("}", "]")
    string_matriz = string_matriz.replace("{", "[")

    matriz = np.array(ast.literal_eval(string_matriz))
    
    arquivo_entrada.close()
    return matriz

def imprime_matriz(matriz, arquivo_saida):
    ''' Imprime uma matriz no formato definido pelo problema em um arquivo de
        saida'''
    string = np.array_str(matriz)
    string = re.sub(' +', ' ', string)

    string = string.replace("[ ", "[")
    string = string.replace(" ]", "]")
    string = string.replace("[", "{")
    string = string.replace("]", "}")
    string = string.replace("\n ", ",")
    string = string.replace(" ", ",")

    print >> arquivo_saida, string
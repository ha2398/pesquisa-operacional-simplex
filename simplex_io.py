"""
@author: Hugo Araujo de Sousa [2013007463]
"""

import numpy as np

def le_matriz_entrada(nome_entrada):
    ''' Le o arquivo de entrada e o transforma em uma matriz Numpy '''

    arquivo_entrada = open(nome_entrada, 'r')
    string_matriz = arquivo_entrada.read()
    
    # Converte a string para o formato de input para Numpy
    string_matriz = string_matriz.replace("},", "};")
    string_matriz = string_matriz.replace("}", "")
    string_matriz = string_matriz.replace("{", "")

    matriz = np.matrix(string_matriz)
    
    arquivo_entrada.close
    return matriz
"""
@author: Hugo Araujo de Sousa [2013007463]
"""

import numpy as np

def read_input_matrix():
    input_name = input("Nome do arquivo de entrada (entre aspas): ")
    
    input_file = open(input_name, 'r')
    
    matrix_string = input_file.read()
    
    # Converte a string para o formato de input para Numpy
    matrix_string = matrix_string.replace("},", "};")
    matrix_string = matrix_string.replace("}", "")
    matrix_string = matrix_string.replace("{", "")

    matrix = np.matrix(matrix_string)
    
    input_file.close
    return matrix

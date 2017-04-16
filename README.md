# Pesquisa Operacional - Trabalho Prático 1 - 1º Semestre de 2017 - UFMG/DCC

**Autor**: [Hugo Sousa](https://github.com/ha2398)

## Descrição

O objetivo deste trabalho é implementar o algoritmo Simplex para resolução de problemas de programação linear.

## Entrada

A entrada do algoritmo será uma matriz da forma

        [ c^T 0 ]
    X = [ A   b ]

escrita no formato {{linha 0}, {linha 1},...,{linha n}}, correspondendo à PL

**max c^T x**

**sujeita a Ax <= b**

**x >= 0**.


## Saída

A saída será produzida em formato .txt. Existem 2 modos distintos para o programa.

No primeiro modo (apropriado para PLs arbitrárias e grandes), há três possibilidades:

a) Se a PL for inviável, o programa imprime:
"PL inviável, aqui está um certificado {certificado}".

b) Se a PL for ilimitada, o programa imprime:
"PL ilimitada, aqui está um certificado {certificado}".

c) Se a PL for viável, o programa imprime:
"Solução ótima x = {solução}, com valor objetivo **valor**, e solução dual y = {solução}".

O segundo modo, somente para PLs viáveis e limitadas, o programa consulta o usuário se ele deseja resolver pelo método simplex primal ou simplex dual.

## Execução

Para executar o programa, é preciso ter o Python 3 instalado.

$ python3 tp1.py <input> <output>

Além disso, pode-se usar a opção make para execução:

$ make ENTRADA=<input> SAIDA=<saida>

Ou, para limpar a pasta de arquivos de saida e arquivos objeto:

$ make clean

## Observações

O programa foi desenvolvido usando Python 3 (3.4.3) como referência.

Pode ser necessária a instalação de pacotes adicionais, como Numpy.
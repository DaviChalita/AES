# Referencias
# https://medium.com/wavy-engineering/building-aes-128-from-the-ground-up-with-python-8122af44ebf9
# https://kavaliro.com/wp-content/uploads/2014/03/AES.pdf

from collections import deque

import numpy as np

chave0 = [int('54', 16), int('68', 16), int('61', 16), int('74', 16), int('73', 16), int('20', 16), int('6D', 16),
          int('79', 16), int('20', 16), int('4B', 16), int('75', 16), int('6E', 16), int('67', 16), int('20', 16),
          int('46', 16), int('75', 16)]

print("Chave Round 0: ", chave0)

texto = [int('54', 16), int('77', 16), int('6F', 16), int('20', 16), int('4F', 16), int('6E', 16), int('65', 16),
         int('20', 16), int('4E', 16), int('69', 16), int('6E', 16), int('65', 16), int('20', 16), int('54', 16),
         int('77', 16), int('6F', 16)]

print("Texto ", texto)

s_box = [
    [int('63', 16), int('7c', 16), int('77', 16), int('7b', 16), int('f2', 16), int('6b', 16), int('6f', 16),
     int('c5', 16), int(
        '30', 16), int('01', 16), int('67', 16), int('2b', 16), int('fe', 16), int('d7', 16), int('ab', 16),
     int('76', 16)],
    [int('ca', 16), int('82', 16), int('c9', 16), int('7d', 16), int('fa', 16), int('59', 16), int('47', 16),
     int('f0', 16), int(
        'ad', 16), int('d4', 16), int('a2', 16), int('af', 16), int('9c', 16), int('a4', 16), int('72', 16),
     int('c0', 16)],
    [int('b7', 16), int('fd', 16), int('93', 16), int('26', 16), int('36', 16), int('3f', 16), int('f7', 16),
     int('cc', 16), int(
        '34', 16), int('a5', 16), int('e5', 16), int('f1', 16), int('71', 16), int('d8', 16), int('31', 16),
     int('15', 16)],
    [int('04', 16), int('c7', 16), int('23', 16), int('c3', 16), int('18', 16), int('96', 16), int('05', 16),
     int('9a', 16), int(
        '07', 16), int('12', 16), int('80', 16), int('e2', 16), int('eb', 16), int('27', 16), int('b2', 16),
     int('75', 16)],
    [int('09', 16), int('83', 16), int('2c', 16), int('1a', 16), int('1b', 16), int('6e', 16), int('5a', 16),
     int('a0', 16), int(
        '52', 16), int('3b', 16), int('d6', 16), int('b3', 16), int('29', 16), int('e3', 16), int('2f', 16),
     int('84', 16)],
    [int('53', 16), int('d1', 16), int('00', 16), int('ed', 16), int('20', 16), int('fc', 16), int('b1', 16),
     int('5b', 16), int(
        '6a', 16), int('cb', 16), int('be', 16), int('39', 16), int('4a', 16), int('4c', 16), int('58', 16),
     int('cf', 16)],
    [int('d0', 16), int('ef', 16), int('aa', 16), int('fb', 16), int('43', 16), int('4d', 16), int('33', 16),
     int('85', 16), int(
        '45', 16), int('f9', 16), int('02', 16), int('7f', 16), int('50', 16), int('3c', 16), int('9f', 16),
     int('a8', 16)],
    [int('51', 16), int('a3', 16), int('40', 16), int('8f', 16), int('92', 16), int('9d', 16), int('38', 16),
     int('f5', 16), int(
        'bc', 16), int('b6', 16), int('da', 16), int('21', 16), int('10', 16), int('ff', 16), int('f3', 16),
     int('d2', 16)],
    [int('cd', 16), int('0c', 16), int('13', 16), int('ec', 16), int('5f', 16), int('97', 16), int('44', 16),
     int('17', 16), int(
        'c4', 16), int('a7', 16), int('7e', 16), int('3d', 16), int('64', 16), int('5d', 16), int('19', 16),
     int('73', 16)],
    [int('60', 16), int('81', 16), int('4f', 16), int('dc', 16), int('22', 16), int('2a', 16), int('90', 16),
     int('88', 16), int(
        '46', 16), int('ee', 16), int('b8', 16), int('14', 16), int('de', 16), int('5e', 16), int('0b', 16),
     int('db', 16)],
    [int('e0', 16), int('32', 16), int('3a', 16), int('0a', 16), int('49', 16), int('06', 16), int('24', 16),
     int('5c', 16), int(
        'c2', 16), int('d3', 16), int('ac', 16), int('62', 16), int('91', 16), int('95', 16), int('e4', 16),
     int('79', 16)],
    [int('e7', 16), int('c8', 16), int('37', 16), int('6d', 16), int('8d', 16), int('d5', 16), int('4e', 16),
     int('a9', 16), int(
        '6c', 16), int('56', 16), int('f4', 16), int('ea', 16), int('65', 16), int('7a', 16), int('ae', 16),
     int('08', 16)],
    [int('ba', 16), int('78', 16), int('25', 16), int('2e', 16), int('1c', 16), int('a6', 16), int('b4', 16),
     int('c6', 16), int(
        'e8', 16), int('dd', 16), int('74', 16), int('1f', 16), int('4b', 16), int('bd', 16), int('8b', 16),
     int('8a', 16)],
    [int('70', 16), int('3e', 16), int('b5', 16), int('66', 16), int('48', 16), int('03', 16), int('f6', 16),
     int('0e', 16), int(
        '61', 16), int('35', 16), int('57', 16), int('b9', 16), int('86', 16), int('c1', 16), int('1d', 16),
     int('9e', 16)],
    [int('e1', 16), int('f8', 16), int('98', 16), int('11', 16), int('69', 16), int('d9', 16), int('8e', 16),
     int('94', 16), int(
        '9b', 16), int('1e', 16), int('87', 16), int('e9', 16), int('ce', 16), int('55', 16), int('28', 16),
     int('df', 16)],
    [int('8c', 16), int('a1', 16), int('89', 16), int('0d', 16), int('bf', 16), int('e6', 16), int('42', 16),
     int('68', 16), int(
        '41', 16), int('99', 16), int('2d', 16), int('0f', 16), int('b0', 16), int('54', 16), int('bb', 16),
     int('16', 16)]
]
# inicializa matriz
estado = [None] * 16

# faz o XOR entre a chave e o texto
for i in range(len(chave0)):
    estado[i] = chave0[i] ^ texto[i]

print("Matriz de estado: ", estado)


def substitui_sbox(byte):
    x = byte >> 4
    y = byte & 15
    return s_box[x][y]


# troca o texto resultante pelo seu correspondente s-box
for i in range(len(estado)):
    estado[i] = substitui_sbox(estado[i])

print("Texto passado pelo S-box: ", estado)

esquerda = 0
ini = 0
fim = 4
rotacionado = deque([])

# faz o shift para a esquerda, sendo a 1a linha com o shift = 0 at?? a ??ltima com shift = 3
# converte para tipo deque para fazer esse shift mais facilmente atrav??s do m??todo rotate
for i in range(len(estado)):
    rot = deque(estado[ini:fim])
    rot.rotate(esquerda)
    esquerda -= 1
    ini += 4
    fim += 4
    rotacionado += rot

print("Resultado rota????o para a esquerda: ", rotacionado)


def multiplica2(v):
    s = v << 1
    s &= 0xff
    if (v & 128) != 0:
        s = s ^ 0x1b
    return s


def multiplica3(v):
    return multiplica2(v) ^ v


def mistura_colunas(matriz):
    nmatriz = [[], [], [], []]
    for i in range(4):
        col = [matriz[j][i] for j in range(4)]
        col = mistura_coluna(col)
        for i in range(4):
            nmatriz[i].append(col[i])
    return nmatriz


def mistura_coluna(coluna):
    r = [
        multiplica2(coluna[0]) ^ multiplica3(coluna[1]) ^ coluna[2] ^ coluna[3],
        multiplica2(coluna[1]) ^ multiplica3(coluna[2]) ^ coluna[3] ^ coluna[0],
        multiplica2(coluna[2]) ^ multiplica3(coluna[3]) ^ coluna[0] ^ coluna[1],
        multiplica2(coluna[3]) ^ multiplica3(coluna[0]) ^ coluna[1] ^ coluna[2],
    ]
    return r


# convert o array rotacionado em numpy array para poder mudar seu formato para um array de 4 x 4
# e assim ser mais f??cil de realizar as pr??ximas opera????es
arrrot = np.asarray(list(rotacionado))
matrot = arrrot.reshape(4, 4)

coluna_misturada = mistura_colunas(matrot)

print("Encripta????o AES resultado Round 0: ", coluna_misturada)
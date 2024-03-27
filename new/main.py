from utils import *
from dict import *


def main():
    nome =  "/workspaces/Compilador-C/new/teste1.c"
    programa = ler_arquivo(nome)
    original = open(nome, 'r')
    print(original.read())


    rules = [find_text_constants, Find_reserved, find_ops, find_numbers, find_delimiters, find_identifiers]
    for rule in rules:
        programa = rule(programa)
        print('\n-----------------\n' + programa + '\n-----------------\n')

if __name__ == "__main__":
    print("----------------- Programa Iniciado -----------------")
    main()
    print("-----------------  Parsed Correctly -------------------")
    print("-----------------------   End   -----------------------")
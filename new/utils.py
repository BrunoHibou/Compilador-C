from dict import *
import re
import sys

def ler_arquivo(teste):
    f = open(teste, 'r')
    program = ""
    buffer = ""
    in_multiline_comment = False
    for line in f:
        i = 0
        while i < len(line):
            if in_multiline_comment:
                # Estamos dentro de um comentário de bloco, ignoramos tudo até encontrar o final do comentário
                if line[i:i + 2] == "*/":
                    in_multiline_comment = False
                    i += 1
            else:
                # Verifica se há um comentário de linha
                if line[i:i + 2] == "//":
                    break  # ignoramos o restante da linha
                elif line[i:i + 2] == "/*":
                    # Início do comentário de bloco
                    in_multiline_comment = True
                    i += 1
                else:
                    program += line[i]  # Adicionamos o caractere à string do programa
            i += 1
        # Adicionamos o buffer ao programa se estivermos no estado DEFAULT
        if not in_multiline_comment:
            program += buffer
            buffer = ""
    f.close()
    return program

def Find_reserved(programa):
    padrao = r"\b(" + "|".join(regex) + r")\b"
    nova_string = re.sub(padrao, lambda match: ' ', programa)
    regex_encontradas = re.findall(padrao, programa)
    universal_printer(regex_encontradas, 'reserved word')
    return nova_string

def find_ops(programa):
    padrao = r"(\s+|)(%s)(\s+|)" % "|".join(map(re.escape, ops))
    ops_encontrados = re.findall(padrao, programa)
    for index, value in enumerate(ops_encontrados):
        ops_encontrados[index] = ops_encontrados[index][1]
    universal_printer(ops_encontrados, 'operator')
    nova_string = re.sub(padrao, lambda match: ' ', programa)
    return nova_string

def find_numbers(programa):
    padrao = regex['numerais']
    numeros_encontrados = re.findall(padrao, programa)
    inteiros = [num for num in numeros_encontrados if '.' not in num]
    floats = [num for num in numeros_encontrados if '.' in num]

    universal_printer(inteiros, 'Inteiro')
    universal_printer(floats, 'Flutuante')

    nova_string = re.sub(padrao, lambda match: ' ', programa)
    return nova_string

def find_text_constants(programa):
    padrao = regex['constantes_textuais']
    constantes_encontradas = re.findall(padrao, programa)
    universal_printer(constantes_encontradas, 'text constant')
    nova_string = re.sub(padrao, lambda match: ' ', programa)
    return nova_string

def find_delimiters(programa):
    padrao = regex['delimitadores']
    delimitadores_encontrados = re.findall(padrao, programa)
    universal_printer(delimitadores_encontrados, 'delimiter')
    nova_string = re.sub(padrao, lambda match: ' ', programa)
    return nova_string

def find_identifiers(programa):
    find_illegal_char(programa)
    find_alphanumerical(programa)
    padrao = regex['identificadores']
    caracteres_identificadores = re.findall(padrao, programa)
    universal_printer(caracteres_identificadores, 'identifier')
    nova_string = re.sub(padrao, lambda match: ' ', programa)
    return nova_string

def find_illegal_char(programa):
    for caractere in programa:
        if caractere not in ops and caractere not in blank and not any(
                re.findall(padrao, caractere) for padrao in regex.values()):
            print(f"Erro: o caractere '{caractere}' não é permitido!")
            sys.exit()

def find_alphanumerical(programa):
    padrao = r'\b(\d+[a-zA-Z0-9_]*)\b'
    palavras_com_numeros = re.findall(padrao, programa)
    for palavra in palavras_com_numeros:
        if re.match('^\d', palavra):
            print(f'Erro: "{palavra}" é uma palavra inválida pois começa com um número.')
            sys.exit()

    return programa

def universal_printer(list, type):
    if not list:
        print(f"None Found: {type}")
    for element in list:
        print(f"'{element}' is a {type}.")


reserved = ["asm",
            "auto",
            "break",
            "case",
            "char",
            "const",
            "continue",
            "default",
            "do",
            "double",
            "else",
            "enum",
            "extern",
            "float",
            "for",
            "goto",
            "if",
            "int",
            "long",
            "register",
            "return",
            "short",
            "signed",
            "sizeof",
            "static",
            "struct",
            "switch",
            "typedef",
            "union",
            "unsigned",
            "void",
            "volatile",
            "while",
            "include"]

ops =  ["+=",
        "-=",
        "++",
        "--",
        "<=",
        ">=",
        "->",
        "==",
        "!=",
        "||",
        "&&",
        "*=",
        "/=",
        "<",
        ">",
        "+",
        "-",
        "=",
        "*",
        "/",
        "%",
        "!",
        "&"
        "%=",
        "<<=",
        ">>=",
        "&=",
        "^="
        ]


blank = [" ",
              "'",
              "\n",
              "	"
              ]

regex = {
    'numerais': r'\b(\d+\.?\d*)\b',
    'caracteres_especiais': r"[\[@&~!#$\^\|{}\]:;<>?,\.']|\(\)|\(|\)|{}|\[\]|\"",
    'identificadores': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'delimitadores': r"[\(\)\[\]\{\};,:]",
    'constantes_textuais': r'"(.*?)"'
}


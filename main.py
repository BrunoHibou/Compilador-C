from lex import Lex
import rules


content = '52132 + )23(())))) - x * 3'

print('parsing content')
print(content)
print('\n\n')

lex = Lexicon(content, [ \
    rules.NumberConstantRule(), \
    rules.SymbolRule(), \
    rules.IdRule() ])

while True:
    token_atual = lex.next()
    if token_atual is None:
        break
    print(f'\ntoken extraido: {token_atual}\n\n\n')

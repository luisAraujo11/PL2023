import ply.lex as lex

states = (
    ('function', 'inclusive'),
    ('while', 'inclusive'),
    ('for', 'inclusive'),
    ('if', 'inclusive'),
    ('program', 'exclusive')
)

tokens = (
    'COMMENT',
    'COMMENTB',  # comentario com barra //
    'FUN',
    'FUNB',  # inicio da funçao
    'FUNE',  # fim da funçao
    'WHILE',
    'WHILEB',  # inicio do while
    'WHILEE',  # fim do while
    'FOR',
    'FORB',  # inicio do for
    'FORE',  # fim do for
    'PROGRAM',
    'PROGRAMB',  # inicio do programa
    'PROGRAME',  # fim do programa
    'ARR',  # array
    'ATR',  # atribuiçao
    'DCL',  # declaraçao
    'ATREDCL',  # atribuiçao e declaraçao
    'IF',
    'IFB',  # inicio do if
    'IFE',  # fim do if
    'FUNEX'  # funçao existente, p.e. print ou outra previamente declarada
)


def t_COMMENT(t):
    r'\/\*[\w\s\.\-\:\b]*\*\/'
    return t


def t_COMMENTB(t):
    r'\/\/[^\n]*'
    return t


def t_ANY_FUN(t):
    r'function\s\w+\([\w]+\)'
    t.lexer.states.append('function')
    t.lexer.begin('function')
    return t


def t_function_FUNB(t):
    r'\{'
    return t


def t_function_FUNE(t):
    r'}'
    t.lexer.states = t.lexer.states[:-1]
    t.lexer.begin(str(t.lexer.states[-1]))
    return t


def t_ANY_WHILE(t):
    r'while\s[\s\w<>]+'
    t.lexer.states.append('while')
    t.lexer.begin('while')
    return t


def t_while_WHILEB(t):
    r'\{'
    return t


def t_while_WHILEE(t):
    r'\}'
    t.lexer.states = t.lexer.states[:-1]
    t.lexer.begin(str(t.lexer.states[-1]))
    return t


def t_ANY_FOR(t):
    r'for\s[\w+]\sin\s\[\d+\.*\d*\]'
    t.lexer.states.append('for')
    t.lexer.begin('for')
    return t


def t_for_FORB(t):
    r'\{'
    return t


def t_for_FORE(t):
    r'\}'
    t.lexer.states = t.lexer.states[:-1]
    t.lexer.begin(str(t.lexer.states[-1]))
    return t


def t_ANY_IF(t):
    r'if\s[\w+\s+<>\[\]]+'
    t.lexer.states.append('if')
    t.lexer.begin('if')
    return t


def t_if_IFB(t):
    r'\{'
    return t


def t_if_IFE(t):
    r'\}'
    t.lexer.states = t.lexer.states[:-1]
    t.lexer.begin(str(t.lexer.states[-1]))
    return t


def t_PROGRAM(t):
    r'program\s[\w]+'
    t.lexer.states.append('program')
    t.lexer.begin('program')
    return t


def t_program_PROGRAMB(t):
    r'\{'
    return t


def t_program_PROGRAME(t):
    r'\}'
    t.lexer.begin('INITIAL')
    t.lexer.states = t.lexer.states[:-1]
    return t


def t_ARR(t):
    r'\w+\[\d+\]\s=\s\{(,*|\d+)+\}'
    return t


def t_ATR(t):
    r'\w+\s=\s[\w\[\]\s*-]+'
    return t


def T_DCL(t):
    r'int\s\w+'
    return t


def t_ANY_ATREDCL(t):
    r'int\s\w+\s=\s[\w+\d,\s+\[\]=\{\}]+'
    return t


def t_ANY_FUNEX(t):
    r'\w+\([\w,\s\(\)]*\)'
    return t


def t_ANY_error(t):
    # print(f'caracter ilegal: {t.value[0]}')
    # print(t.value[0], end="")
    t.lexer.skip(1)


lexer = lex.lex()
lexer.states = ['INITIAL']

data1 = '''
/* factorial.p
-- 2023-03-20 
-- by jcr
*/

int i;

// Função que calcula o factorial dum número n
function fact(n){
  int res = 1;
  while res > 1 {
    res = res * n;
    res = res - 1;
  }
}

// Programa principal
program myFact{
  for i in [1..10]{
    print(i, fact(i));
  }
}
'''

data2 = '''
/* max.p: calcula o maior inteiro duma lista desordenada
-- 2023-03-20 
-- by jcr
*/

int i = 10, a[10] = {1,2,3,4,5,6,7,8,9,10};

// Programa principal
program myMax{
  int max = a[0];
  for i in [1..9]{
    if max < a[i] {
      max = a[i];
    }
  }
  print(max);
}
'''

lexer.input(data1 + data2)

# print('Tokens:')

while tok := lexer.token():
    print(tok)
    # print('states: ' + str(lexer.states))

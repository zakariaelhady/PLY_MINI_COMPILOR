import ply.lex as lex

class MyLexer():

    # CONSTRUCTOR
    def __init__(self):
        self.lexer = lex.lex(module=self)

    tokens=(
    'NAME','NUMBER','STRING',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS','MODULO',
    'LPAREN','RPAREN','LBRACKET','RBRACKET','LACCOLADE','RACCOLADE',
    'EQUAL','NOTEQ','LARGE','SMALL','LRGEQ','SMLEQ',
    'SEMICOLON','COMMA','COMMENT','PERIOD',
    'DECREMENT','INCREMENT'
    )

    reserved = {
        'ma7da' : 'WHILE',
        'igh': 'IF',
        'ighorili': 'ELSE',
        'ara' : "PRINT",
        'gher':'INPUT',
        'kism':'CLASS',
        'kaygat':'FOR',
        'tawori':'FUNCTION',
        'rar':'RETURN',
        'ighorili_igh' : 'ELIF', 
        'd' : 'AND', 
        'ighd' : 'OR', 
        'is7a'  : 'TRUE',                           
        'ighlt'  : 'FALSE',
        'ar':'TO',
        'azmozl':'STEP',
        '_3amm':'PUBLIC',
        '_5ass':'PRIVATE',
        'ikossa':'EXTENDS',
    }
    tokens += tuple(reserved.values())
    # Tokens
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_EQUALS  = r'='

    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_LBRACKET  = r'\['
    t_RBRACKET  = r'\]'
    t_LACCOLADE=r'\{'
    t_RACCOLADE=r'\}'

    t_EQUAL   = r'\=\='
    t_NOTEQ   = r'\!\='
    t_LARGE   = r'\>'
    t_SMALL   = r'\<'
    t_LRGEQ   = r'\>\='
    t_SMLEQ   = r'\<\='
    t_MODULO= r'%'
    t_SEMICOLON=r'\;'
    t_COMMA=r','
    t_PERIOD=r'.'

    t_DECREMENT=r'\-\-'
    t_INCREMENT=r'\+\+'

    def t_NUMBER(self,t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_NAME(self,t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        if t.value in self.reserved:
            t.type = self.reserved[t.value]
        return t

    def t_STRING(self,t):
        r'"[^"]*"'
        t.value = t.value[1:len(t.value) - 1]
        return t

    def t_COMMENT(self,t):
        r'\#.*'
        pass

    def t_TRUE(self,t):
        r'is7a'
        t.value = True
        return t

    def t_FALSE(self,t):
        r'ighlt'
        t.value = False
        return t

    # Ignored characters
    t_ignore = " \t"

    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self,t):
        print(f"Illegal character {t.value[0]!r}")
        t.lexer.skip(1)
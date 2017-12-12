# coding=UTF-8
########################################
## Jennifer Izabel Rodrigues de Souza ##
##           Compiladores             ##
##         Analisador Léxico          ##
########################################


import sys
import ply.lex as lex

class Lexer:

  def __init__(self):
    self.lexer = lex.lex(debug=False, module=self, optimize=False)

  #lista com as palavras reservadas
  reservadas = {
  	'se'		: 'SE',
  	'então'		: 'ENTAO',
  	'senão'		: 'SENAO',
  	'fim' 		: 'FIM',
  	'retorna' 	: 'RETORNA',
  	'repita' 	: 'REPITA',
  	'até' 		: 'ATE',
    'leia' 		: 'LEIA',
    'escreve' 	: 'ESCREVE',
    'flutuante' : 'FLUTUANTE',
    'inteiro' 	: 'INTEIRO'
  }

  # Lista dos nomes de tokens
  tokens = [
     'SOMA',
     'SUBTRACAO',
     'MULTIPLICACAO',
     'DIVISAO',
     'IGUALDADE',
     'VIRGULA',
     'ATRIBUICAO',
     'MENOR',
     'MAIOR',
     'MENOR_IGUAL',
     'MAIOR_IGUAL',
     'MENOR_MAIOR',
     'ABRE_PAR',
     'FECHA_PAR',
     'DOIS_PONTOS',
     'ABRE_COL',
     'FECHA_COL',
     'E_LOGICO',
     'OU_LOGICO',
     'NEGACAO',
     'NUMERO_INTEIRO',
     'NUMERO_FLUTUANTE',
     'NUMERO_NOTACAO_CIENTIFICA',
     'IDENTIFICADOR',
     'COMENTARIO',
  ]+ reservadas.values() #adiciona as palavras reservadas na lista de tokens


  # Regras de expressão regular dos tokens simples
  t_ignore  		= ' \t' # Uma string contendo caracteres ignorados (espaços e tabs)
  t_SOMA 			= r'\+' 
  t_SUBTRACAO 	= r'-'
  t_MULTIPLICACAO = r'\*'
  t_DIVISAO 		= r'/'
  t_IGUALDADE 	= r'\='
  t_VIRGULA 		= r','
  t_ATRIBUICAO 	= r':\='
  t_MENOR 		= r'\<'
  t_MAIOR 		= r'\>'
  t_MENOR_IGUAL 	= r'\<\='
  t_MAIOR_IGUAL 	= r'\>\='
  t_MENOR_MAIOR   = r'\<\>'
  t_ABRE_PAR 		= r'\('
  t_FECHA_PAR 	= r'\)'
  t_DOIS_PONTOS 	= r'\:'
  t_ABRE_COL 		= r'\['
  t_FECHA_COL 	= r'\]'
  t_E_LOGICO 		= r'&&'
  t_OU_LOGICO 	= r'\|\|'
  t_NEGACAO 		= r'\!'


  # Regras de expressão regular dos tokens mais complexos
  def t_NUMERO_NOTACAO_CIENTIFICA(self, t):
      r'[\d]+[e][\d]*'
      t.value = float(t.value)    
      return t

  def t_NUMERO_FLUTUANTE(self, t):
      r'[\d]+[\.][\d]*'
      t.value = float(t.value)    
      return t

  def t_NUMERO_INTEIRO(self, t):
      r'[\d]+'
      t.value = int(t.value)    
      return t

  def t_IDENTIFICADOR(self, t):
      r'[a-zA-Z][_a-zA-Z0-9à-ú]*'
      t.type = self.reservadas.get(t.value,'IDENTIFICADOR')
      return t

  def t_COMENTARIO(self, t): 
      r'\{[^}]*[^{]*\}'
      t.value = (t.value) 

  def t_novalinha(self, t):
      r'\n+'
      t.lexer.lineno += len(t.value)

  # Error handling rule
  def t_error(self, t):
      print("caracter não suportado '%s', linha %d, coluna %d" % (t.value[0],  t.lineno, t.lexpos))
      t.lexer.skip(1)

  def open_arquivo(self, filename): #função auxiliar para abertura e leitura de arquivo
  	string = ""
  	file = open(filename, "r") 
  	for line in file: 
  		string += line
  	return string



  def test(self, code):
    lex.input(code)
    while True:
        t = lex.token()
        if not t:
            break
        print(t)

if __name__ == '__main__':
    from sys import argv
    lexer = Lexer()
    f = open(argv[1])
    lexer.test(f.read())

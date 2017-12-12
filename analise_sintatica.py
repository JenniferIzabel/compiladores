# -*- coding: utf-8 -*-
########################################
## Jennifer Izabel Rodrigues de Souza ##
##           Compiladores             ##
##       Analisador Sintático         ##
########################################

# verificar erro 5, 6 e expressoes.tpp

from ply import yacc
import sys
from analise_lexica import Lexer
from graphviz import Digraph

class tree:

    def __init__(self, type_node, child=[], value=''):
        self.type = type_node
        self.child = child
        self.value = value

    def __str__(self):
        return self.type
    
    
class parser:

    def __init__(self, code):
        lex = Lexer()
        self.tokens = lex.tokens
        self.precedence = (
            ('nonassoc', 'IGUALDADE', 'NEGACAO', 'MAIOR_IGUAL', 'MENOR_IGUAL', 'MENOR', 'MAIOR'),
            ('left', 'SOMA', 'SUBTRACAO'),
            ('left', 'MULTIPLICACAO', 'DIVISAO'),
        )
        parser = yacc.yacc(debug=False, module=self, optimize=False)
        self.ast = parser.parse(code)

    def p_top(self, p):
        '''
        top : programa
            | lista_declaracoes
        '''
        p[0] = tree('top', [p[1]])
        

    def p_programa(self, p):
        'programa : lista_declaracoes'
        p[0] = tree('programa', [p[1]])


    def p_lista_declaracoes_1(self, p):
        'lista_declaracoes :  declaracao'
        p[0] = tree('lista_declaracoes_1', [p[1]])

    def p_lista_declaracoes_2(self, p):
        'lista_declaracoes : lista_declaracoes declaracao'
        p[0] = tree('lista_declaracoes_2', [p[1], p[2]])

    def p_declaracao(self, p):
        '''
        declaracao : declaracao_variaveis
                    | inicializacao_variaveis
                    | declaracao_funcao 
        '''
        p[0] = tree('declaracao', [p[1]]) 

    def p_declaracao_variaveis(self, p):
        'declaracao_variaveis : tipo DOIS_PONTOS lista_variaveis'
        p[0] = tree('declaracao_variaveis', [p[1], p[3]])

    def p_inicializacao_variaveis(self, p):
        'inicializacao_variaveis : atribuicao '

        p[0] = tree('inicializacao_variaveis', [p[1]]) 

    def p_lista_variaveis_1(self, p):
        'lista_variaveis : var'       
        p[0] = tree('lista_variaveis_1', [p[1]])
    
    def p_lista_variaveis_2(self, p):
        'lista_variaveis : lista_variaveis VIRGULA var  '
        p[0] = tree('lista_variaveis_2', [p[1], p[3]])

    def p_var_1(self, p):
        'var : IDENTIFICADOR '
        p[0] = tree('var_1',[], p[1])
       
    def p_var_2(self, p):
        'var : IDENTIFICADOR indice  '
        p[0] = tree('var_2', [p[2]], p[1])


    def p_indice_1(self, p):
        'indice : indice ABRE_COL expressao FECHA_COL '
        p[0] = tree('indice_1', [p[1],p[3]])
 
    def p_indice_2(self, p):
        'indice : ABRE_COL expressao FECHA_COL '
        p[0] = tree('indice_2', [p[2]])

    def p_tipo1(self,p):
        'tipo : INTEIRO'
        p[0] = tree('inteiro')

    def p_tipo2(self,p):
        'tipo : FLUTUANTE'
        p[0] = tree('flutuante')

    def p_tipo3(self,p):
        'tipo : NUMERO_NOTACAO_CIENTIFICA'
        p[0] = tree('notacao_cientifica')

    def p_declaracao_funcao_1(self, p):
        'declaracao_funcao : tipo cabecalho'
        p[0] = tree('declaracao_funcao_1', [p[1], p[2]])

    def p_declaracao_funcao_2(self, p):
        'declaracao_funcao : cabecalho '
        p[0] = tree('declaracao_funcao_2', [p[1]])

    def p_cabecalho(self, p):
        'cabecalho : IDENTIFICADOR ABRE_PAR lista_parametros FECHA_PAR corpo FIM'

        p[0] = tree('cabecalho', [p[3],p[5]],p[1])

    def p_lista_parametros_1(self, p):
        'lista_parametros : lista_parametros VIRGULA parametro '
        p[0] = tree('lista_parametros_1', [p[1], p[3]])


    def p_lista_parametros_2(self, p):
        '''lista_parametros : parametro
                            | vazio   '''
        p[0] = tree('lista_parametros_2', [p[1]])


    def p_parametro_1(self, p):
        'parametro : tipo DOIS_PONTOS IDENTIFICADOR '
        p[0] = tree('parametro_1', [p[1]], p[3])
       
    def p_parametro_2(self, p):
        'parametro : parametro ABRE_COL FECHA_COL '
        p[0] = tree('parametro_2', [p[1]])

    def p_corpo_1(self, p):
        'corpo : corpo acao '
        p[0] = tree('corpo_1', [p[1], p[2]])

    def p_corpo_2(self, p):
        'corpo : vazio '
        p[0] = tree('corpo_2', [p[1]])

    def p_acao(self, p):
        '''acao : expressao
                | declaracao_variaveis
                | se 
                | repita
                | leia 
                | escreva
                | retorna
                | error 
                | comentario'''

        p[0] = tree('acao', [p[1]]) 

    def p_comentario(self, p):
        'comentario : COMENTARIO'
        p[0] = tree('comentario', [p[1]])

    def p_se_1(self, p):
        "se : SE expressao ENTAO corpo FIM"
        p[0] = tree('se_1', [p[2], p[4]])

    def p_se_2(self, p):
        "se : SE expressao ENTAO corpo SENAO corpo FIM"
        p[0] = tree('se_2',[p[2], p[4], p[6]])


    def p_repita(self, p):
        'repita : REPITA corpo ATE expressao '

        p[0] = tree('repita', [p[2], p[4]])

    def p_atribuicao(self, p):
        'atribuicao : var ATRIBUICAO expressao  '

        p[0] = tree('atribuicao', [p[1], p[3]]) 

    def p_leia(self, p):
        'leia : LEIA ABRE_PAR IDENTIFICADOR FECHA_PAR '

        p[0] = tree('leia', [], p[3]) 

    def p_escreva(self, p):
        'escreva : ESCREVE ABRE_PAR expressao FECHA_PAR  '

        p[0] = tree('escreva', [p[3]]) 

    def p_retorna(self, p):
        'retorna : RETORNA ABRE_PAR expressao FECHA_PAR   '

        p[0] = tree('retorna', [p[3]]) 

    def p_expressao(self, p):
        '''expressao : expressao_simples
                        | atribuicao   '''

        p[0] = tree('expressao', [p[1]]) 

    def p_expressao_simples_1(self, p):
        'expressao_simples : expressao_aditiva '
        p[0] = tree('expressao_simples_1', [p[1]])

    def p_expressao_simples_2(self, p):
        'expressao_simples : expressao_simples operador_relacional expressao_aditiva '
        p[0] = tree('expressao_simples_2', [p[1], p[2], p[3]])

    def p_expressao_aditiva_1(self, p):
        'expressao_aditiva : expressao_multiplicativa'
        p[0] = tree('expressao_aditiva_1', [p[1]])

    def p_expressao_aditiva_2(self, p): 
        'expressao_aditiva : expressao_aditiva operador_soma expressao_multiplicativa '
        p[0] = tree('expressao_aditiva_2', [p[1], p[2], p[3]])

    def p_expressao_multiplicativa_1 (self, p):
        'expressao_multiplicativa  : expressao_unaria '
        p[0] = tree('expressao_multiplicativa_1', [p[1]])

    def p_expressao_multiplicativa_2 (self, p):
        'expressao_multiplicativa  : expressao_multiplicativa operador_multiplicacao expressao_unaria '
        p[0] = tree('expressao_multiplicativa_2', [p[1], p[2], p[3]])

    def p_expressao_unaria_1 (self, p):
        'expressao_unaria  : fator '
        p[0] = tree('expressao_unaria_1', [p[1]])

    def p_expressao_unaria_2 (self, p):
        'expressao_unaria  : operador_soma fator '
        p[0] = tree('expressao_unaria_2', [p[1], p[2]])    

    def p_expressao_unaria_e (self, p):
        'expressao_unaria : expressao E_LOGICO expressao'
        p[0] = tree('expressao_unaria_e', [p[1], p[3]])

    def p_expressao_unaria_ou (self, p):
        'expressao_unaria : expressao OU_LOGICO expressao'
        p[0] = tree('expressao_unaria_ou', [p[1], p[3]])

    def p_expressao_unaria_neg (self, p):
        'expressao_unaria : NEGACAO expressao'
        p[0] = tree('expressao_unaria_neg', [p[3]])
    

    def p_operador_relacional (self, p):
        '''operador_relacional  : MENOR
                                | MAIOR 
                                | IGUALDADE
                                | MENOR_MAIOR 
                                | MENOR_IGUAL
                                | MAIOR_IGUAL   '''

        p[0] = tree('operador_relacional', [], p[1])

    def p_operador_soma (self, p):
        '''operador_soma  : SOMA 
                            | SUBTRACAO '''

        p[0] = tree('operador_soma', [], p[1]) 

    def p_operador_multiplicacao  (self, p):
        '''operador_multiplicacao  : MULTIPLICACAO
                                        | DIVISAO '''

        p[0] = tree('operador_multiplicacao', [], p[1]) 

    def p_fator_1 (self, p):
        'fator  : ABRE_PAR expressao FECHA_PAR '
        p[0] = tree('fator_1', [p[2]])

    def p_fator_2 (self, p):
        '''fator  :  var 
                    | chamada_funcao
                    | numero '''
        p[0] = tree('fator_2', [p[1]], p[1])

    def p_numero  (self, p):
        '''numero  : NUMERO_INTEIRO 
                    | NUMERO_FLUTUANTE 
                    | NUMERO_NOTACAO_CIENTIFICA '''

        p[0] = tree('numero',[], p[1]) 

    def p_chamada_funcao  (self, p):
        'chamada_funcao  : IDENTIFICADOR ABRE_PAR lista_argumentos FECHA_PAR '

        p[0] = tree('chamada_funcao', [p[3]], p[1]) 

    def p_lista_argumentos_1 (self, p):
        'lista_argumentos : lista_argumentos VIRGULA expressao '
        p[0] = tree('lista_argumentos_1', [p[1], p[3]])

    def p_lista_argumentos_2 (self, p):
        'lista_argumentos : expressao '
        p[0] = tree('lista_argumentos_2', [p[1]])

    
    

    def p_vazio(self, p):
        'vazio :'
        pass

    def p_error(self, p):
        if p:
            print("erro sintático: não foi possível reconher '%s' na linha %d" % (p.value, p.lineno))
        else:
            yacc.restart()
            print("erro sintático: definições incompletas!")

def print_tree(node,level=0):
    if node != None:
        print("%s %s" % ('\t' * level, node.type))
        for child in node.child: 
            print_tree(child,level+1)

def verArvoreTexto(node,w,i):
    if node != None:
        value1 = node.type + str(i)
        i = i + 1
        for son in node.child:
            w.edge(value1,str(son) + str(i))
            verArvoreTexto(son,w,i)

if __name__ == '__main__':
    from sys import argv, exit
    f = open(argv[1])
    arvore = parser(f.read())
    #print_tree(arvore.ast)

    w = Digraph('G', filename='./Saidas/ArvoreRepr.gv')
    verArvoreTexto(arvore.ast,w,i = 0)
    w.view()


    file_object = open("./Saidas/SaidaArvore.txt", "w")
    file_object.write(w.source)
    file_object.close()

    
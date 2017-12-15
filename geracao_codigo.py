# -*- coding: utf-8 -*-
########################################
## Jennifer Izabel Rodrigues de Souza ##
##           Compiladores             ##
##  Gerador de Código Intermediário   ##
########################################
from analise_sintatica import parser
from analise_sintatica import tree
from analise_semantica import *
from llvmlite import ir
from ctypes import CFUNCTYPE, c_int32


class Geracao:
	def __init__(self, code):
		Arvore = parser(code)
		self.ArvoreSintatica = Arvore.ast
		sema = Semantica(code)
		self.dicionarioSimbolos = sema.dicionarioSimbolos
		self.lista_parametros = sema.lista_parametros
		self.module = ir.Module('modulo.bc')
		self.inteiro = ir.IntType(32)
		self.flutuante = ir.FloatType()
		self.void = ir.VoidType()
		self.align = 4
		self.funcao = None 
		self.vleia = None
		self.vescreva = None
		self.entryBlock = None
		self.endBasicBlock = None
		self.builder = None
		self.escopo = "global"
		self.valor_retorno = 0

		self.i = 0 #auxilia atributos funcoes

		print("\nGERAÇÃO\n")
		self.programa(self.ArvoreSintatica)

	def programa(self, node):
		self.lista_declaracoes(node.child[0])

	def lista_declaracoes(self, node):
		if node.type == "lista_declaracoes_1":
			self.declaracao(node.child[0])
		elif node.type == "lista_declaracoes_2":
			self.lista_declaracoes(node.child[0])
			self.declaracao(node.child[1])

	def declaracao(self, node):
		#print("->declaracao")
		aux = node.child[0]
		if aux.type == "declaracao_variaveis":
			tipo = node.child[0].child[0]
			self.lista_variaveis(aux, tipo)
		elif aux.type == "declaracao_funcao_1" or aux.type == "declaracao_funcao_2":
			self.declaracao_funcao(aux)			
		elif aux.type == "inicializacao_variaveis":
			#print("-->inicializacao_variaveis")
			tipo = node.child[0].child[0]
			atribuicao = node.child[0].child[1]
			atribuicao(atribuicao, tipo)

	def lista_variaveis(self, node, tipo):
		#print("->lista_variaveis")
		if(node.child[1].type == "lista_variaveis_1"):
			var = str(node.child[1].child[0].value)
			tipo = tipo.type

			if (self.escopo == "global"):
				if(tipo == "inteiro"):
					v = ir.GlobalVariable(self.module, self.inteiro,var)
					v.initializer = ir.Constant(self.inteiro, 0)
					v.linkage = "common"
					v.align = self.align
				elif(tipo == "flutuante"):
					v = ir.GlobalVariable(self.module, self.flutuante,var)
					v.initializer =  ir.Constant(self.flutuante, 0.0)
					v.linkage = "common"
					v.align = self.align
			
		elif(node.child[1].type == "lista_variaveis_2"):
			var = str(node.child[1].child[0].value)
			tipo = tipo.type
						


	def declaracao_funcao(self, node):
		#print("->declaracao_funcao")
		nome_func = node.child[1].value
		self.escopo = nome_func

		if (nome_func == "principal"):
			func_principal = ir.FunctionType(self.inteiro, ()) # Cria função principal
			self.funcao = ir.Function(self.module, func_principal, name=nome_func) # Declara função principal

			self.entryBlock = self.funcao.append_basic_block('entry') # Declara o bloco de entrada

			self.builder = ir.IRBuilder(self.entryBlock) # Adiciona o bloco de entrada

			self.cabecalho(node.child[1]) #executa o bloco todo da funcao

		else:
			if(node.type == "declaracao_funcao_1"):
				#print("->declaracao_funcao_1")
				tipo = node.child[0].type
				
				if(tipo == "inteiro"):
					func = ir.FunctionType(self.inteiro, ()) # Cria função tipo inteiro

				elif(tipo == "flutuante"):
					func = ir.FunctionType(self.flutuante, ()) # Cria função tipo flutuante

				self.funcao = ir.Function(self.module, func, name=nome_func) # Declara função
				self.entryBlock = self.funcao.append_basic_block('entry') # Declara o bloco de entrada
				self.builder = ir.IRBuilder(self.entryBlock) # Adiciona o bloco de entrada

				self.cabecalho(node.child[1])
			else:
				#print("->declaracao_funcao_2")
				func = ir.FunctionType(self.void, ()) # Cria função tipo void

				self.funcao = ir.Function(self.module, func, name=nome_func) # Declara função
				self.entryBlock = self.funcao.append_basic_block('entry') # Declara o bloco de entrada
				self.builder = ir.IRBuilder(self.entryBlock) # Adiciona o bloco de entrada

				
				self.cabecalho(node.child[0]) #executa o bloco todo da funcao

		#fazendo o retorno da funcao
		self.endBasicBlock = self.funcao.append_basic_block('exit')
		self.builder.branch(self.endBasicBlock)
		self.builder.position_at_end(self.endBasicBlock)

		if(type(self.valor_retorno) == int):
			v = self.builder.alloca(self.inteiro, name='retorno')
		else:
			v = self.builder.alloca(self.flutuante, name='retorno')

		x =  ir.Constant(self.inteiro, self.valor_retorno)
		self.builder.store(x, v)
		returnVal_temp = self.builder.load(v, name='', align=self.align)
		self.builder.ret(returnVal_temp)


	def cabecalho(self, node):
		#print("-->cabecalho")
		self.i = 0
		nome_func = node.value
		self.lista_parametros(node.child[0], nome_func)
		self.corpo(node.child[1])

	def lista_parametros(self, node, nome_func):
		#print("-->lista_parametros")
		if(node.type == "lista_parametros_1"):
			print("ENTROU")
			for (k,v) in self.lista_parametros.items():
				if (k == nome_func):
					for(key, val) in v:
						x = val.split(".")
						tipo = x[0]
						var = x[1]
						if(tipo == "inteiro"):
							v = ir.GlobalVariable(self.module, self.inteiro,var)
							v.initializer = ir.Constant(self.inteiro, 0)
							v.linkage = "common"
							v.align = self.align
						elif(tipo == "flutuante"):
							v = ir.GlobalVariable(self.module, self.flutuante,var)
							v.initializer =  ir.Constant(self.flutuante, 0.0)
							v.linkage = "common"
							v.align = self.align
			
		else:
			pass



	def corpo(self, node):
		#print("-->corpo")
		if(node.type == "corpo_1"):
			self.corpo(node.child[0])
			self.acao(node.child[1])
		

	def acao(self, node):
		#print("-->acao")
		acao = node.child[0]
		if(acao.type == "expressao"):
			self.expressao(acao)
		elif(acao.type == "declaracao_variaveis"):
			tipo = node.child[0].child[0]
			self.lista_variaveis(acao, tipo)
		elif(acao.type == "se"):
			print("se")

		elif(acao.type == "repita"):
			print("repita")

		elif(acao.type == "leia"):
			self.leia()

		elif(acao.type == "escreva"):
			self.escreva()

		elif(acao.type == "retorna"):
			self.valor_retorno = self.val_ret(self.escopo)

	def leia(self):
		print("-->leia")

	def escreva(self):
		print("-->escreva")

	def val_ret(self, func):
		#print("-->valor variavel")
		for (k,v) in self.dicionarioSimbolos.items():
				if (k == func):
					return v[2]
		return 0
		
	def atribuicao(self, node):
		#print("->atribuicao")
		var = node.child[0].value[0]
		for (k,v) in self.dicionarioSimbolos.items():
				va = k.split(".")
				if (len(va) > 1 and var == va[1]):
					if(v[1]=="inteiro"):
						val = ir.Constant(self.inteiro, v[2]) #v[2] = valor da variavel 
						var = self.builder.alloca(self.inteiro, name=var)
					else:
						val = ir.Constant(self.flutuante, v[2]) #v[2] = valor da variavel 
						var = self.builder.alloca(self.flutuante, name=var)
					self.builder.store(val, var)

	def expressao(self, node):
		#print("->expressao")
		aux = node.child[0]
		if(aux.type == "atribuicao"):
			self.atribuicao(aux)
		elif(aux.type == "expressao_simples_1"):
			self.expressao_aditiva(aux.child[0])
		elif(aux.type == "expressao_simples_2"):
			self.expressao(aux.child[0])
			self.expressao_aditiva(aux.child[0])
		

	def expressao_aditiva(self, node):
		#print("->expressao_aditiva")
		if(node.type == "expressao_aditiva_1"):
			self.expressao_multiplicativa(node.child[0])
		elif(node.type == "expressao_aditiva_2"):
			adt = node.child[0]
			op = node.child[1].value
			mult = node.child[2]
			self.expressao_aditiva(adt)
			self.expressao_multiplicativa(mult)

		else:
			pass


	def expressao_multiplicativa(self, node):
		#print("->expressao_multiplicativa")
		if(node.type == "expressao_multiplicativa_1"):
			self.expressao_unaria(node.child[0])
		elif(node.type == "expressao_multiplicativa_2"):
			mult = node.child[0]
			op = node.child[1].value
			una = node.child[2]
			self.expressao_multiplicativa(mult)
			self.expressao_unaria(una)
		else:
			pass

	def expressao_unaria(self, node):
		#print("->expressao_unaria")
		if(node.type == "expressao_unaria_1"):
			self.fator(node.child[0])
		elif(node.type == "expressao_unaria_2"):
			op = node.child[0].child[0].value
			self.fator(node.child[1])
		elif(node.type == "expressao_unaria_e"):
			self.expressao(node.child[0])
			self.expressao(node.child[1])
		elif(node.type == "expressao_unaria_ou"):
			self.expressao(node.child[0])
			self.expressao(node.child[1])
		elif(node.type == "expressao_unaria_neg"):
			self.expressao(node.child[0])
		else:
			pass

	def fator(self, node):
		#print("->fator")
		if(node.type == "fator_1"):
			self.numero(node.child[0])
			self.valor = node.child[0].value
		elif(node.type == "fator_2"):
			if(node.child[0].type == "var_1" or node.child[0] == "var_2"):
				self.numero(node.child[0])
			elif(node.child[0].type == "chamada_funcao"):
				self.chamada_funcao(node.child[0].child[0])
			elif(node.child[0].type == "numero"):
				self.valor = node.child[0].value
				self.numero(node.child[0])
		else:
			pass

	
	def numero(self, node):
		#print("->numero")
		if(node.value == "NUMERO_INTEIRO"):
			tipo = "inteiro"
		elif(node.value == "NUMERO_FLUTUANTE"):
			tipo = "flutuante"
		elif(node.value == "NUMERO_NOTACAO_CIENTIFICA"):
			tipo = "cientifico"
		return node.value

	def chamada_funcao(self, node):#############
		print("->chamada_funcao")


if __name__ == '__main__':
    from sys import argv, exit
    f = open(argv[1])
    s = Geracao(f.read())
    f = open('saida.ll', 'w')
    f.write(str(s.module))
    f.close()
    print("\nSAIDA\n")
    print(s.module) 
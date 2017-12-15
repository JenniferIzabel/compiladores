# -*- coding: utf-8 -*-
########################################
## Jennifer Izabel Rodrigues de Souza ##
##           Compiladores             ##
##       Analisador Semantico         ##
########################################

from analise_sintatica import parser
from analise_sintatica import tree

class Semantica: 
	def __init__(self, code):
		Arvore = parser(code)
		self.ArvoreSintatica = Arvore.ast
		self.dicionarioSimbolos = {} #{escopo.nome,[estrutura, tipo, valor, utilizada]} 
		self.parametros_funcoes = {} #{nome,[tipo_param1, tipo+param2]}
		self.escopo = "global" # inicia no escopo global
		self.valor = 0 # auxiliar para atribuir valor as variaveis
		self.i = 0 #auxilia atributos funcoes
		self.inicioSimbolos()
		self.checa_variaveis(self.dicionarioSimbolos)
		self.checa_funcoes(self.dicionarioSimbolos)
		self.possui_principal(self.dicionarioSimbolos)
		self.print_dicionario(self.dicionarioSimbolos)


	def inicioSimbolos (self):
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
			#print("->lista_variaveis_1")
			#verifica se a variavel ja existe 
			if self.escopo+'.'+var in self.dicionarioSimbolos.keys():
				print("Erro semântico: variável "+var+" já declarada no escopo "+self.escopo)
			else:
				self.dicionarioSimbolos[self.escopo+'.'+var] = ['variavel',tipo.type,0,False]
		elif(node.child[1].type == "lista_variaveis_2"):
			var = str(node.child[1].child[0].value)
			#verifica se a variavel ja existe 
			if self.escopo+'.'+var in self.dicionarioSimbolos.keys():
				print("Erro semântico: variável "+var+" já declarada no escopo "+self.escopo)
			else:
				self.dicionarioSimbolos[self.escopo+'.'+var] = ['variavel',tipo.type,0,False]
			


	def declaracao_funcao(self, node):
		#print("->declaracao_funcao")
		nome_func = node.child[1].value
		#verifica se o metodo já existe 
		if nome_func in self.dicionarioSimbolos.keys():
			print("Erro semântico: função já declarada com o nome "+nome_func)
		else:
			self.escopo = nome_func
			if(node.type == "declaracao_funcao_1"):
				#print("->declaracao_funcao_1")
				tipo = node.child[0].type
				self.dicionarioSimbolos[nome_func] = ['funcao',tipo,0,False, False]
				self.cabecalho(node.child[1])
			else:
				#print("->declaracao_funcao_2")
				self.dicionarioSimbolos[nome_func] = ['funcao','void',0,True, False]
				self.cabecalho(node.child[0])

	def cabecalho(self, node):
		#print("-->cabecalho")
		self.i = 0
		nome_func = node.value
		self.lista_parametros(node.child[0], nome_func)
		self.corpo(node.child[1])

	def lista_parametros(self, node, nome_func):
		#print("-->lista_parametros")
		if(node.type == "lista_parametros_1"):
			self.lista_parametros(node.child[0], nome_func)
			self.parametro(node.child[1], nome_func)
		else:
			if(node.child[0] != None):
				self.parametro(node.child[0], nome_func)


	def parametro(self, node, nome_func):
		#print("-->parametro ")
		if(node.type == "parametro_1"):
			tipo = node.child[0]
			var = node.value
			b = False

			for (k,v) in self.parametros_funcoes.items():
				if(k == nome_func):
					v.append(str(tipo)+"."+var) #[tipo.nome_var1, tipo.nome_var2]
					b = True
			if(b == False):
				self.parametros_funcoes[nome_func] = [tipo]
		else:
			self.parametro(node.child[0])

		if self.escopo+'.'+var in self.dicionarioSimbolos.keys():
			print("Erro semântico: variável "+var+" já declarada no escopo "+self.escopo)
		else:
			self.dicionarioSimbolos[self.escopo+'.'+var] = ['variavel',tipo.type,0,False]

	def corpo(self, node):		
		if(node.type == "corpo_1"):
			self.corpo(node.child[0])
			self.acao(node.child[1])

			
		if(node.type == "corpo_2"):
			pass

		

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
			print("leia")

		elif(acao.type == "escreva"):
			print("escreva")

		elif(acao.type == "retorna"):
			n = self.expressao(acao.child[0])
			self.atribui_retorno(n)

	def se_senao(self, node):
		#print("-->se_senao")
		exp = node.child[0]
		corpo = node.child[1]
		self.expressao(exp)
		self.corpo(corpo)



	def atribui_retorno(self, n):
		#print("->atribui retorno")
		for (k,v) in self.dicionarioSimbolos.items():
				va = k.split(".")
				if (k == self.escopo):
					if(type(n) == int):
						tipo = "inteiro"
					elif(type(n) == float):
						tipo = "flutuante"
					else:
						print("Erro semântico: Tipo incompatível")
						tipo = "incompativel"
						pass
					if(v[1] == tipo):
						v[2] = n
						v[4] = True
						self.valor = 0
					else:
						print("Erro semântico: Função do tipo "
							+v[1]+" tentando retornar valor "+tipo)

	def valor_variavel(self, var):
		#print("-->valor variavel")
		for (k,v) in self.dicionarioSimbolos.items():
				va = k.split(".")
				if (len(va) > 1 and var.value == va[1]):
					return v[2]
		return 0

	def atribuicao(self, node):
		#print("->atribuicao")
		var = node.child[0].value[0]
		n = self.expressao(node.child[1]) # vai calcular o valor
		x = False 
		for (k,v) in self.dicionarioSimbolos.items():
				va = k.split(".")
				if (len(va) > 1 and var == va[1]):
					x = True
					v[3] = True #variavel utilizada
					#checa o tipo
					s = self.vtipo()
					if(v[1] == s):
						v[2] = n
						self.valor = 0
						return n
					else:
						print("Erro semântico: tentativa de atribuição de valor "
							+s+" para variável "+v[1])

		if x == False: #variavel não existe
			print("Erro semântico: variável "+var+" não declarada")

	def vtipo(self):
		x = (type(self.valor))
		if (x == float):
			return "flutuante"
		elif (x == int):
			return "inteiro"

	def expressao(self, node):
		#print("->expressao")
		aux = node.child[0]
		if(aux.type == "atribuicao"):
			self.atribuicao(aux)
		elif(aux.type == "expressao_simples_1"):
			n = self.expressao_aditiva(aux.child[0])
			return n
		elif(aux.type == "expressao_simples_2"):
			a = self.expressao(aux.child[0])
			op = aux.child[1]
			b = self.expressao_aditiva(aux.child[2])
			print ("SE "+a, op, b)
		try:		
			aux2 = node.child[1]
			if(aux2.type == "expressao_simples_1"):
				n = self.expressao_aditiva(aux2.child[0])
				return n
			elif(aux2 != None and aux2.type == "expressao_simples_2"):
				self.expressao(aux2.child[0])
				n = self.expressao_aditiva(aux2.child[0])
				return n
		except:
			pass

	def expressao_aditiva(self, node):
		#print("->expressao_aditiva")
		if(node.type == "expressao_aditiva_1"):
			return self.expressao_multiplicativa(node.child[0])
		elif(node.type == "expressao_aditiva_2"):
			adt = node.child[0]
			op = node.child[1].value
			mult = node.child[2]
			a = self.expressao_aditiva(adt)
			b = self.expressao_multiplicativa(mult)

			if(op == "+"):
				return a + b
			else:
				return a - b
		elif(node.type == "expressao_multiplicativa_1"):
			n = expressao_unaria(node.child[0])
			return n
			pass


	def expressao_multiplicativa(self, node):
		#print("->expressao_multiplicativa")
		if(node.type == "expressao_multiplicativa_1"):
			a =  self.expressao_unaria(node.child[0])
			return a
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
			return self.fator(node.child[0])
		elif(node.type == "expressao_unaria_2"):
			op = node.child[0].child[0].value
			return self.fator(node.child[1])
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
			if(node.child[0].type == "var_1"):
				self.numero(node.child[0])
				var = node.child[0].value

				for (k,v) in self.dicionarioSimbolos.items():
					aux = k.split(".")
					if(len(aux) > 1 and aux[1] == var):
						
						v[3] = True

				n = self.valor_variavel(node.child[0])
				return n
			elif(node.child[0] == "var_2"):#vetor IMPLEMENTAR
				self.numero(node.child[0])
				var = node.child[0].value
				
				for (k,v) in self.dicionarioSimbolos.items():
					aux = k.split(".")
					if(len(aux) > 1 and aux[1] == var):
						v[3] = True

				return node.child[0].value
			elif(node.child[0].type == "chamada_funcao"):
				v = self.chamada_funcao(node.child[0].child[0])
				return v
			elif(node.child[0].type == "numero"):
				self.valor = node.child[0].value
				self.numero(node.child[0])
				return self.valor
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

	def chamada_funcao(self, node):
		print("->chamada_funcao")


		return 0
	
	def checa_variaveis(self, dicio):
		#{escopo.nome,[estrutura, tipo, utilizada]} 
		for (k,v) in dicio.items():
			if (v[0] == "variavel"):
				if (v[3] == False):
					escopo = k.split(".")
					if (escopo[0] != "global"):
						print("Aviso: variável "+escopo[1] + " do escopo "+escopo[0] +" nunca é utilizada")
						pass
					else:
						print("Aviso: variável "+escopo[1] + " do escopo "+escopo[0]+" nunca é utilizada")
						pass

	def checa_funcoes(self, dicio):
		for (k,v) in dicio.items():
			try:
				if (v[4] == False):
						print ("Erro semântico, função "+k+" não está retornando nada")
			except:
				continue
			if (v[0] == "funcao" and k != "principal"):
				if (v[3] == False):
					print("AVISO: função "+k+ " não utilizada'")



	def possui_principal(self, dicio):
		if ("principal" not in dicio.keys()):
			print ("Erro semântico,  Não possui função principal()")

	def print_dicionario(self, dicio):
		print("\nTABELA")
		for (i,j) in dicio.items():
			print(i,j)


if __name__ == '__main__':
    from sys import argv, exit
    f = open(argv[1])
    s = Semantica(f.read())
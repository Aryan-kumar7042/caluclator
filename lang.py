class Token:
	def __init__(self, value, type):
		self.value=value
		self.type=type

class Lexer(object):
	def __init__(self, text):
		self.pos=0
		self.text=text
		try:
			self.current_char=self.text[self.pos]
		except:
			self.pos=None
			self.current_char=None
		self.len=len(text)
		self.op_list={
				'+':'PLUS',
				'-':'MINUS',
				'*':'MUL',
				'/':'DIV'
		}
	def advance(self):
		if self.pos>=self.len-1:
			self.pos=None
			self.current_char=None
		else:
			self.pos+=1
			self.current_char=self.text[self.pos]
	def skip_space(self):
		while self.current_char!=None and self.current_char.isspace():
			self.advance()
		return True
	def integer(self):
		num=''
		while self.current_char!=None and self.current_char.isdigit():
			num+=self.current_char
			self.advance()
		return int(num)
	def next(self):
		while self.current_char!=None:
			if self.current_char.isspace():
				self.skip_space()
				continue
			elif self.current_char.isdigit():
				return Token(self.integer(), "INT")
			elif self.current_char in self.op_list:
				text=self.current_char
				self.advance()
				return Token(text, self.op_list[text])
			else:
				raise Exception("Invalid syntax")
		return Token(None, "EOF")
class ASTNode(object):
	def __init__(self, value, type, left=None, right=None):
		self.value=value
		self.type=type
		self.left=left
		self.right=right
class AST(Lexer):
	def __init__(self, lexer):
		self.lex=lexer
		self.current_tkn=self.lex.next()
		self.token_arr=[]
		self.loop=0
	def advance(self):
		self.current_tkn=self.lex.next()
	def verify(self):
		self.loop=0
		prev_tkn_type=''
		while self.current_tkn.value!=None:
			# verification
			if self.loop==0 and self.current_tkn.value in self.lex.op_list:
				raise Exception("Expected '{}' after a numeric".format(self.current_tkn.value))
			if prev_tkn_type=="OP" and self.current_tkn.value in self.lex.op_list:
				raise Exception("Got operator multiple time")
			self.token_arr.append(self.current_tkn)
			self.loop+=1
			if self.current_tkn.type=="INT":
				prev_tkn_type="INT"
			if self.current_tkn.value in self.lex.op_list:
				prev_tkn_type="OP"
			self.advance()
		if prev_tkn_type=="OP":
			self.token_arr.clear()
			raise Exception("Operator at the end")
		return True
	def ast_construct(self):
		ast.verify()

text="55*85+49"
lex=Lexer(text)
ast=AST(lex)
ast.ast_construct()
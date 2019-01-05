#installare :
#sympy

from lark import Lark, Transformer
import sympy as sym

grammar = """start: expr
             expr: add  | sub | term
             term: mul  | div |  term2
             term2: pow | frac | fact
             fact: value | round_paren_expr | box_paren_expr   | curly_paren_expr
             round_paren_expr: "(" expr ")"     
             box_paren_expr:   "[" expr "]"   
             curly_paren_expr: "{" expr "}"
             pow:  term2 "^" fact
             mul:  term "*" term2
             div:  term ":" term2
             frac: term2 "/" fact
             add:  term "+" expr
             sub:  term "-" expr
             value : SIGNED_NUMBER           
             %import common.SIGNED_NUMBER             
             %import common.WS
             %ignore WS
            
              """



class toOp_transformer(Transformer):
    def expr(self, terms): 
        return (terms[0])
    def term2(self, terms): 
        return (terms[0])
    def term(self, terms): 
        return (terms[0])
    def fact(self, terms): 
        return (terms[0])
    def round_paren_expr(self, terms): 
        return [0,"()", terms[0]]
    def box_paren_expr(self, terms): 
        return [0,"[]", terms[0]]
    def curly_paren_expr(self, terms): 
        return [0,"{}", terms[0]]


    def mul(self, terms):                
        return [0,"*", terms[0], terms[1]]
    def add(self, terms):                
        return [0,"+", terms[0], terms[1]]
    def sub(self, terms):                
        return [0,"-", terms[0], terms[1]]
    def frac(self, terms):                
        return [0,"/", terms[0], terms[1]]
    def div(self, terms):                
        return [0,":", terms[0], terms[1]]
    def pow(self, terms):                
        return [0,"^", terms[0], terms[1]]
    def value(self, val):
        val  = float(val[0])
        if val.is_integer():
            return int(val)
        else:
            return val

def assign_depth(node, n):
    node[0] = n
    a = n
    b = n
    if (type(node[2]) == list ):
        a = assign_depth(node[2],n+1)
    if not (node[1] in ["()","[]","{}"]):
        if (type(node[3]) == list ):
            b = assign_depth(node[3],n+1)

    return max(a,b)
        
def compute_node(node):
    if node[1] == "+":
        return node[2] + node[3]
    elif node[1] == "-":
        return node[2] - node[3]
    elif node[1] == "*":
        return node[2] * node[3]
    elif node[1] == ":":
        return node[2] / node[3]
    elif node[1] == "/":
        return node[2] / node[3]
    elif node[1] == "^":
        return node[2]**node[3]
    elif node[1] == "()":
        return node[2] 
    elif node[1] == "[]":
        return node[2] 
    elif node[1] == "{}":
        return node[2] 

def simplify_node(node):
    if node[1] == "+":
        return sym.simplify(sym.simplify(node[2])+sym.simplify(node[3]))
    elif node[1] == "-":
        return sym.simplify(sym.simplify(node[2])-sym.simplify(node[3]))
    elif node[1] == "*":
        return sym.simplify(sym.simplify(node[2])*sym.simplify(node[3]))
    elif node[1] == ":":
        return sym.simplify(sym.simplify(node[2])/sym.simplify(node[3]))
    elif node[1] == "/":
        return sym.simplify(sym.simplify(node[2])/sym.simplify(node[3]))
    elif node[1] == "^":
        return sym.simplify(sym.simplify(node[2])**sym.simplify(node[3]))
    elif node[1] == "()":
        return node[2]
    elif node[1] == "[]":
        return node[2]
    elif node[1] == "{}":
        return node[2]

def print_expr_tree(node):
    a = "" 
    b = ""
    if (type(node[2]) == list ):
        a = print_expr_tree(node[2])
        if node[1] == "()":        
            a = "("+a+")"
        elif node[1] == "[]":        
            a = "["+a+"]"
        elif node[1] == "{}":        
            a = "{"+a+"}"
    else:
        a = str(node[2])

    if not (node[1] in ["()","[]","{}"]):
        if (type(node[3]) == list ):
            b = print_expr_tree(node[3])
        else:
            b = str(node[3])
        res = a + node[1] + b 
    else:
        res = a

    return res

def gen_latex_expr(node):
    a = "" 
    b = ""
    if (type(node[2]) == list ):
        a = gen_latex_expr(node[2])
        if node[1] == "()":        
            a = "\left("+sym.latex(a)+"\\right)"
        elif node[1] == "[]":        
            a = "\left["+sym.latex(a)+"\\right]"
        elif node[1] == "{}":        
            a = "\left\{"+sym.latex(a)+"\\right\}"
    else:
        a = sym.latex(node[2])

    if not (node[1] in ["()","[]","{}"]):
        if (type(node[3]) == list ):
            b = gen_latex_expr(node[3])
        else:
            b = sym.latex(node[3])

        if node[1] == "+" :
            res = sym.latex(a) + " + " + sym.latex(b )
        elif node[1] == " - " :
            res = sym.latex(a) + "-" + sym.latex(b )
        elif node[1] == "*" :
            res = sym.latex(a) + " \\cdot " + sym.latex(b )
        elif node[1] == ":" :
            res = sym.latex(a) + " : " + sym.latex(b )
        elif node[1] == "/" :
            res = " \\frac {{{:}}} {{{:}}} ".format(sym.latex(a),sym.latex(b)) 
        elif node[1] == "^" :
            res = " {{{:}}}^{{{:}}} ".format(sym.latex(a),sym.latex(b)) 
    else:
        res = sym.latex(a)

    return res


def solve_tree_at_depth(node, n):
    if (type(node[2]) == list ):
        if node[2][0]== n:
            node[2] =  compute_node(node[2])
        else:
            solve_tree_at_depth(node[2],n)
    if not (node[1] in ["()","[]","{}"]):
        if (type(node[3]) == list ):
            if node[3][0]== n:
                node[3] =  compute_node(node[3])
            else:
                solve_tree_at_depth(node[3],n)

def simplify_tree_at_depth(node, n):
    if (type(node[2]) == list ):
        if node[2][0]== n:
            node[2] =  simplify_node(node[2])
        else:
            simplify_tree_at_depth(node[2],n)
    if not (node[1] in ["()","[]","{}"]):
        if (type(node[3]) == list ):
            if node[3][0]== n:
                node[3] =  simplify_node(node[3])
            else:
                simplify_tree_at_depth(node[3],n)


parser = Lark(grammar)

def calc(val):
    tree = parser.parse(val)
    op_tree = toOp_transformer().transform(tree)
    root = op_tree.children[0]
    steps = []     
    if type(root) == list:
        max_depth = assign_depth(root,0)


        print("max_depth:"+ str(max_depth))
        math_latex =  gen_latex_expr(root)
        steps.append(math_latex)
        for i in range(max_depth):      
            simplify_tree_at_depth(root, max_depth-i)        
            math_latex =  gen_latex_expr(root)
            steps.append(math_latex)
        #ultimo passaggio
        root = simplify_node(root)
    steps.append(sym.latex(root))
    return steps


if  __name__ == "__main__":
    line = "2+3/4^4/8+6"
    print(solve_expr(line))






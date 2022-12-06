import ast
from itertools import permutations
from visitors.GlobalVariables import GlobalVariableExtraction
import string

class LocalVariableExtraction(GlobalVariableExtraction):
    """ 
        We extract all function arguments, local variables and 
    """

    def __init__(self, vars) -> None:
        super().__init__()
        self.local = dict()  
        self.args = set() 
        self.vars = vars
        self.r_num = 0
        self.re = False
        self.gen = self.get_name()
        
    def visit_Assign(self, node):
        if len(node.targets) != 1:
            raise ValueError("Only unary assignments are supported")

        var = node.targets[0].id
        if (var in self.vars or len(var) > 8): # rename
            name = self.get_next()
            var = name                
            # self.vars[node.targets[0].id] = var
            self.local[node.targets[0].id] = var
        else:
            self.local[node.targets[0].id] = var
        

    def visit_FunctionDef(self, node):
        arguments = node.args.args
            
        for arg in arguments:
            self.visit(arg)
        
        for contents in node.body:
            self.visit(contents)
    
    def visit_arg(self, node):
        var = node.arg
        if (var not in self.vars):
            if (len(var)> 8):  #checks if the variable name is greater than 8 characters long
                name = self.get_next()
                var = name
            self.vars[node.arg] = var
            node.arg = var
        
        self.args.add(node.arg) 
    
    def visit_Return(self, node):
        self.re = 'r'+str(self.retun_num())
        # self.vars[self.re] = ''

    ####
    ## Helper functions for renaming generator
    ####
    def get_name(self):
        i = 0  # length of new rename
        possible = []

        while i <= 8:
            for p in possible:
                yield ''.join(p)
            i += 1
            possible = permutations(string.ascii_uppercase, i)  #only permutate all the possible names of length n

    def get_next(self):
        next_name = next(self.gen)
        while (next_name in self.vars):
            next_name = next(self.gen)

        return next_name
    
    def retun_num(self):
        self.r_num = self.r_num + 1
        return self.r_num
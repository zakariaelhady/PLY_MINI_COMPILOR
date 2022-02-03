from myLexer import *
import ply.yacc as yacc


class MyParser:

    # CONSTRUCTOR
    def __init__(self,lexer):
        self.parser = yacc.yacc(module=self)
        self.lexer = lexer

    
    tokens = MyLexer.tokens


        
    # Precedence rules for the arithmetic operators
    precedence = (
        ('left','PLUS','MINUS'),
        ('left','TIMES','DIVIDE'),
        ('right','UMINUS'),
        )

    # dictionary of names (for storing variables)
    variables={}

    def p_statements(self,p):
        ''' statements : statements statement
                    | statement
        '''
        if len(p)==3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]]


    def p_statement(self,p):
        '''statement : assignement
                    | print'''
        p[0] = p[1]

    def p_assignement(self,p):
        'assignement : NAME EQUALS expression_string SEMICOLON'
        self.variables[p[1]]=p[3]

    def p_assignement_incrementation(self,p):
        'assignement : NAME INCREMENT SEMICOLON'
        self.variables[p[1]]=self.variables[p[1]] + 1


    def p_assignement_decrementation(self,p):
        'assignement : NAME DECREMENT SEMICOLON'
        self.variables[p[1]]=self.variables[p[1]] - 1
    
    
    def p_expression_string(self,p):
        ''' expression_string : expression
                                | STRING
                                | boolean'''
        p[0] = p[1]

    ####################################INPUT###################################
    def p_command_read(self,p):
        '''assignement : NAME EQUALS INPUT LPAREN  RPAREN SEMICOLON'''
        var = input()
        self.variables[p[1]]=var

    ####################################PRINT#################################
    def p_printing(self,p):
        'print : PRINT LPAREN  expression_string RPAREN SEMICOLON'
        p[0] = p[3]

    ######################################################## OP  ########################################

    def p_expression_paren(self,p):
        'expression : LPAREN  expression RPAREN'
        p[0] = p[2]

    def p_expression_op(self,p):
        '''expression : expression PLUS expression
                        | expression MINUS expression
                        | expression TIMES expression
                        | expression DIVIDE expression
                        | expression MODULO expression
        '''
        if p[2] == '+'  : p[0] = p[1] + p[3]
        elif p[2] == '-': p[0] = p[1] - p[3]
        elif p[2] == '*': p[0] = p[1] * p[3]
        elif p[2] == '/': 
            if p[3]!=0:
                p[0] = p[1] / p[3]
            else: p[0]="can't divide by zero"
        elif p[2]=='%': p[0] = p[1] % p[3]

    def p_expression_term(self,p):
        'expression : term'
        p[0] = p[1]

    def p_term_factor(self,p):
        '''term : factor
                '''
        p[0] = p[1]

    def p_term_NAME(self,p):
        'term : NAME'
        p[0] = self.variables[p[1]]

    def p_factor_num(self,p):
        'factor : NUMBER'
        p[0] = p[1]
    ##########
    def p_expr_uminus(self,p):
        'uminus : MINUS NUMBER %prec UMINUS'
        p[0] = -p[2]
    def p_term_uminus(self,p):
        'factor : uminus'
        p[0] = p[1]

    ###############################################  Arrays  ###########################################################

    def p_assignement_array(self,p):
        ' assignement : array'
        p[0] = p[1]

    def p_array(self,p):
        ''' array : NAME EQUALS LBRACKET RBRACKET SEMICOLON
            | NAME EQUALS array_content SEMICOLON
        '''
        if(len(p)==6):
            self.variables[p[1]]=[]
        else:
            self.variables[p[1]]=p[3]

    def p_array_content(self,p):
        ' array_content : LBRACKET elements RBRACKET'
        p[0] = p[2]

    def p_elements(self,p):
        ''' elements : element COMMA elements
                        | element
        '''
        stmts=[]
        if (len(p) == 2):
            stmts.append(p[1])
        else:
            stmts.append(p[1])
            stmts.extend(p[3])

        p[0] =stmts

    def p_element_exp_str(self,p):
        ''' element : expression_string
                    | array_content
        '''
        p[0] = p[1]
    
    def p_array_index(self,p):
        ' array_index : LBRACKET expression RBRACKET'
        p[0] = p[2]
    def p_element_return(self,p): 
        ''' expression_string : NAME array_index
                                | NAME  array_index array_index
        '''
        if(len(p)==3):
            p[0] = self.variables[p[1]][p[2]]
        else:
            p[0] = self.variables[p[1]][p[2]][p[3]]

    def p_assignement_change_element_array(self,p):
        ' assignement : change_element_array '
        p[0] = p[1]

    def p_change_element_array(self,p):
        ''' change_element_array : NAME array_index EQUALS element SEMICOLON
                                    | NAME array_index array_index EQUALS element SEMICOLON
        '''
        if(len(p)==6):
            if self.variables[p[1]]==[]:
                values=[]
                values.append(p[4])
                self.variables[p[1]]=values
            else:
                self.variables[p[1]][p[2]]=p[4]
        else:
            self.variables[p[1]][p[2]][p[3]]=p[5]
    ################################################################booleans##############################
    def p_boolean(self,p):
        ''' boolean : TRUE
                    | FALSE
        '''
        p[0] = p[1]

    def p_booleans(self,p):
        '''booleans : booleans AND boolean
                    | booleans OR boolean
                    | boolean
                    | LPAREN  booleans RPAREN

                    '''
        if len(p) == 2:
            p[0] = p[1]
        elif p[2]=="d":
            p[0] = p[1] and p[3]
        elif p[2]=="ighd":
            p[0] = p[1] or p[3]
        elif p[1]=='(':
            p[0] = p[2]


    def p_comparison(self,p):
        '''boolean : expression_string EQUAL expression_string
                | expression_string NOTEQ expression_string
                | expression_string LARGE expression_string
                | expression_string SMALL expression_string
                | expression_string LRGEQ expression_string
                | expression_string SMLEQ expression_string
                '''
        if p[2] == '==':
            p[0] = p[1] == p[3]
        elif p[2]=='!=':
            p[0] = p[1] != p[3]
        elif p[2] == '>':
            p[0] = p[1] > p[3]
        elif p[2] == '<':
            p[0] = p[1] < p[3]
        elif p[2] == '>=':
            p[0] = p[1] >= p[3]
        elif p[2] == '<=':
            p[0] = p[1] <= p[3]
        


    ################################################## PARTIE IF ##############################"
    def p_else(self,p):
        'else : ELSE LACCOLADE statements RACCOLADE'
        p[0]=p[3]

    def p_elif(self,p):
        'elif : ELIF LPAREN  booleans RPAREN LACCOLADE statements RACCOLADE'
        if p[3]:
            p[0]=p[6]

    def p_elifs(self,p):
        '''elifs : elifs elif
                | elif
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            if p[1] is None :
                p[0] = p[2]
            elif p[2] is None :
                p[0] = p[1]
            else:
                p[0] = p[1] + [p[2]]




    def p_if(self,p):
        '''if : IF LPAREN  booleans RPAREN LACCOLADE statements RACCOLADE
        '''
        if p[3]:
            p[0] = p[6]

    def p_statement_if(self,p):
        '''statement :  if
                    | if elifs
                    | if elifs else
                    '''
        if len(p) == 2:
            p[0] = p[1]

        elif len(p) == 3:
            if p[1] is not None :
                p[0] = p[1]
            elif p[1] is None and p[2] is not None:
                p[0] = p[2]

        elif len(p) == 4:
            if p[1] is not None :
                p[0] = p[1]
            elif p[1] is None and p[2] is not None :
                p[0] = p[2]
            else :   #p[1] is None and p[2] is None
                p[0] = p[3]

    def p_statement_if_else(self,p):
        '''statement :  if else
                    '''
        if p[1] is not None :
            p[0] = p[1]
        else:  # p[1] is None
            p[0] = p[2]
    ################################################## WHILE ##############################"
    def p_statement_while(self,p):
        'statement : loop_while'
        p[0]=p[1]
    
    def p_loop_while(self,p):
        'loop_while : WHILE booleans LACCOLADE statements  RACCOLADE'
        i=0
        stmts=[]
        while p[2]:
            stmts.append(p[4])
            i=i+1
            if (i == 20):
                print("Infinite loop")
                break
        p[0] = stmts


    ##########################################################################  FOR LOOP  ##################################
    #for(i=0 ar 9,azmozl=3){}
    def p_for_loop(self,p):
        '''statement : FOR LPAREN  NAME EQUALS expression TO expression COMMA STEP EQUALS expression RPAREN LACCOLADE statements RACCOLADE'''
        stmts= []
        if p[7] > p[5]:
            i = 0
            while i < p[7]-p[5]:
                stmts.append(p[14])
                i = i+int(p[11])
            p[0] =stmts
        else:
            p[0]="error :index {} > {}".format(p[5],p[7])

    #for(i=0 ar 9){}
    def p_for_loop2(self,p):
        '''statement : FOR LPAREN  NAME EQUALS expression TO expression RPAREN LACCOLADE statements RACCOLADE'''
        stmts = []
        if p[7] > p[5]:
            for i in range(p[7]-p[5]):
                stmts.append(p[10])
            p[0] =stmts
        else:
            p[0]="erreur :index {} > {}".format(p[5],p[7])
    #################################################### Function  ################################

    def p_argument_list(self,p):
        '''
            argument_list : expression
                        | argument_list COMMA expression
        '''
        stmts=[]
        if (len(p) == 2):
            stmts.append(p[1])
        else:
            stmts.append(p[1])
            stmts.extend([p[3]])
        p[0] =stmts

    def p_parameter(self,p):
        '''
        parameter : NAME
        '''
        p[0] = p[1]


    def p_parameter_list(self,p):
        '''
            parameter_list : parameter
                        | parameter_list COMMA parameter
        '''
        stmts=[]
        if (len(p) == 2):
            stmts.append(p[1])
        else:
            stmts.append(p[1])
            stmts.extend(p[3])
        p[0] =stmts

    functions={}
    def p_func(self,p):
        '''statement : FUNCTION NAME LACCOLADE statements RACCOLADE
                | FUNCTION NAME LACCOLADE statements return RACCOLADE
                | FUNCTION  NAME SMALL parameter_list LARGE LACCOLADE statements RACCOLADE
                | FUNCTION  NAME SMALL parameter_list LARGE LACCOLADE statements return RACCOLADE
        '''
        if(len(p) == 6):
            self.functions[p[2]]=p[4]
        elif(len(p) == 9):
            self.functions[p[2]]=p[7]
        elif(len(p) == 7):
            self.functions[p[2]]=p[5]
        elif(len(p) == 10):
            self.functions[p[2]]=p[8]

    def p_appel_func(self,p):
        '''
        statement : NAME LPAREN argument_list RPAREN  SEMICOLON
                | NAME LPAREN  RPAREN SEMICOLON

        '''
        if p[1] in self.functions:
            p[0] = self.functions[p[1]]
        else:
            p[0]="function not declared !!"

    def p_return(self,p):
        '''
        return : RETURN LPAREN expression RPAREN SEMICOLON
        '''
        p[0]=p[3]

    ######################################   CLASS  #############################
    classes={}
    objects={}
    vars={}
    #{class: vars}
    #{objet:class}
    #{var:value}
    def p_class_vars(self,p):
        '''class_vars : class_vars class_var
                    | class_var
            '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]
    #{var:value}
    def p_class_variables(self,p):
        ''' class_var : PUBLIC NAME EQUALS NUMBER SEMICOLON
                        | PRIVATE NAME EQUALS NUMBER SEMICOLON
        '''
        self.vars[p[2]]=p[4]
        p[0]=p[2]
        
    #{class: vars}
    def p_class(self,p):
        '''statement : CLASS NAME LACCOLADE class_vars RACCOLADE
                    | CLASS NAME EXTENDS NAME LACCOLADE class_vars RACCOLADE
        '''
        if len(p)==6:
            self.classes[p[2]]=p[4]
        else:
            self.classes[p[2]]=p[6]+self.classes[p[4]]

    #{objet:class}
    def p_declare_object(self,p):
        '''
        statement : NAME SMALL NAME LARGE SEMICOLON
        '''
        if p[1] in self.classes:
            self.objects[p[3]]=p[1]
        else:
            p[0]=f"There is no class named' {p[1]} '"

    def p_call_object_var(self,p):
        '''statement : NAME PERIOD NAME SEMICOLON
        '''
        if p[1] in self.objects:
            class_name=self.objects[p[1]]
            if class_name in self.classes:
                class_vars=self.classes[class_name]
                if p[3] in class_vars :
                        value=self.vars[p[3]]
                        p[0]=value
                else:
                    p[0]=f"' {p[3]} ' is not a variable of the class {class_name}"
            else:
                p[0]=f"There is no class named' {class_name} '"
        else:
            p[0]=f"There is no object named' {p[1]} '"

    # Error rule for syntax errors
    def p_error(self,p):
        try:
            print(f"Syntax error at {p.value!r} ")
        except:
            print(f"Exception at {p.value!r} ")


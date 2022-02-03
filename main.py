import sys
from myLexer import MyLexer
from myParser import MyParser

myLex = MyLexer()
myPars = MyParser(myLex)

lex = myLex.lexer
parser = myPars.parser

# data = '''#comment
# #############################classes
# kism MYCLASS{
#     _3amm x=3;
#     _5ass y=5;
# }
# MYCLASS <s>;
# s.x;
# s.y;

# kism classfils ikossa MYCLASS{
#     _3amm var=2;
# }
# classfils <fils>;
# fils.var;
# fils.x;
# '''


#input file
# myFile = open('input.txt')
# data=myFile.read()


# result = parser.parse(data)
# if result is not None:
#     for r in result:
#         if r == None:
#             continue;
#         else:
#             if isinstance(r, list) and None in r:
#                 for i in r:
#                     if i is not None:
#                         print(i)  
#             else:
#                 print(r)



# for GUI

def main():
    args = sys.argv
    input_file=args[1]
    data = open(input_file).read()
    result = parser.parse(data)
    if result is not None:
        for r in result:
            if r == None:
                continue
            else:
                if isinstance(r, list) and None in r:
                    for i in r:
                        if i is not None:
                            print(i)  
                else:
                    print(r)


if __name__ == '__main__':
    main()
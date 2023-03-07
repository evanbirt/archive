# CS3210 - Principles of Programming Languages - Spring 2020
# Author(s): Evan Birt
# Description: parses a c-like grammar and displays tree if correct
# References: started from lex-template.py
# Issues: quickly done -> it's buggy (pending fixes)

from enum import IntEnum
import sys

# done
# all char classes
class CharClass(IntEnum):
    EOF        = 0
    LETTER     = 1
    DIGIT      = 2
    OPERATOR   = 3
    QUOTE      = 5
    BLANK      = 6
    DELIMITER  = 7
    FLOATP     = 8
    COMPARE    = 9
    OTHER      = 10

# done
# all tokens
class Token(IntEnum):
    EOF             = 0
    INT_TYPE        = 1
    MAIN            = 2
    OPEN_PAR        = 3
    CLOSE_PAR       = 4
    OPEN_CURLY      = 5
    CLOSE_CURLY     = 6
    OPEN_BRACKET    = 7 
    CLOSE_BRACKET   = 8
    COMMA           = 9
    ASSIGNMENT      = 10
    SEMICOLON       = 11
    IF              = 12
    ELSE            = 13
    WHILE           = 14
    OR              = 15
    AND             = 16
    EQUALITY        = 17
    INEQUALITY      = 18
    LESS            = 19
    LESS_EQUAL      = 20
    GREATER         = 21
    GREATER_EQUAL   = 22
    ADD             = 23
    SUBTRACT        = 24
    MULTIPLY        = 25
    DIVIDE          = 26
    BOOL_TYPE       = 27
    FLOAT_TYPE      = 28
    CHAR_TYPE       = 29
    IDENTIFIER      = 30
    INT_LITERAL     = 31
    TRUE            = 32
    FALSE           = 33
    FLOAT_LITERAL   = 34
    CHAR_LITERAL    = 35

# done
lookupToken = {
    "int"       : Token.INT_TYPE,    
    "bool"      : Token.BOOL_TYPE,
    "float"     : Token.FLOAT_TYPE,
    "char"      : Token.CHAR_TYPE,
    "main"      : Token.MAIN,
    "if"        : Token.IF,
    "while"     : Token.WHILE,
    "else"      : Token.ELSE,
    "true"      : Token.TRUE,
    "false"     : Token.FALSE,
    "&&"        : Token.AND,
    "||"        : Token.OR,
    "="         : Token.ASSIGNMENT,
    "=="        : Token.EQUALITY,
    "!="        : Token.INEQUALITY,
    "<"         : Token.LESS,
    "<="        : Token.LESS_EQUAL,
    ">"         : Token.GREATER,
    ">="        : Token.GREATER_EQUAL,
    "+"         : Token.ADD,
    "*"         : Token.MULTIPLY,
    "/"         : Token.DIVIDE,
    "("         : Token.OPEN_PAR,
    ")"         : Token.CLOSE_PAR,
    "{"         : Token.OPEN_CURLY,
    "}"         : Token.CLOSE_CURLY,
    "["         : Token.OPEN_BRACKET,
    "]"         : Token.CLOSE_BRACKET,
    ";"         : Token.SEMICOLON,
    ","         : Token.COMMA,
}

# done
# a tree-like data structure
class Tree:
    TAB = "   "
    def __init__(self):
        self.data     = None
        self.children = []

    def add(self, child):
        self.children.append(child)

    def print(self, tab = ""):
        if self.data != None:
            print(tab + self.data)
            tab += self.TAB
            for child in self.children:
                if isinstance(child, Tree):
                    child.print(tab)
                else:
                    print(tab + child)

# done
# error code to message conversion function
def errorMessage(code):
    msg = "Error " + str(code).zfill(2) + ": "
    if code == 1:
        return msg + "Source file missing"
    if code == 2:
        return msg + "Couldn't open source file"
    if code == 3:
        return msg + "Lexical error"
    if code == 4:
        return msg + "Digit expected"
    if code == 5:
        return msg + "Symbol missing"
    if code == 6:
        return msg + "EOF expected"
    if code == 7:
        return msg + "'}' expected"
    if code == 8:
        return msg + "'{' expected"
    if code == 9:
        return msg + "')' expected"
    if code == 10:
        return msg + "'(' expected"
    if code == 11:
        return msg + "main expected"
    if code == 12:
        return msg + "int type expected"
    if code == 13:
        return msg + "']' expected"
    if code == 14:
        return msg + "int literal expected"
    if code == 15:
        return msg + "'[' expected"
    if code == 16:
        return msg + "identifier expected"
    if code == 17:
        return msg + "';' expected"
    if code == 18:
        return msg + "'=' expected"
    if code == 19:
        return msg + "identifier, if, or while expected"
# Error code 99
    return msg + "syntax error"

# done
# reads the next char from input and returns its class
def getChar(input):
    if len(input) == 0:
        return (None, CharClass.EOF)
    c = input[0].lower()
    if c.isalpha():
        return (c, CharClass.LETTER)
    if c.isdigit():
        return (c, CharClass.DIGIT)
    if c in [ '+', '-', '*', '/']:
        return (c, CharClass.OPERATOR)
    if c in ['(', ')', '{', '}', '[', ']']:
        return (c, CharClass.DELIMITER)
    if c in [' ', '\n', '\t']:
        return (c, CharClass.BLANK)
    if c in ['.']:
        return (c, CharClass.FLOATP)
    if c in ['"', "'"]:
        return (c, CharClass.QUOTE)
    if c in ['=', '!', '<', '>']:
        return (c, CharClass.COMPARE)
    return (c, CharClass.OTHER)

# done
# calls getChar and addChar until it returns a non-blank
def getNonBlank(input):
    ignore = ""
    while True:
        c, charClass = getChar(input)
        if charClass == CharClass.BLANK:
            input, ignore = addChar(input, ignore)
        else:
            return input

# done
# adds the next char from input to lexeme, advancing the input by one char
def addChar(input, lexeme):
    if len(input) > 0:
        lexeme += input[0]
        input = input[1:]
    return (input, lexeme)

# done
# returns the next (lexeme, token) pair or ("", EOF) if EOF is reached
def lex(input):
    input = getNonBlank(input)
    c, charClass = getChar(input)
    lexeme = ""

    # checks EOF
    if charClass == CharClass.EOF:
        return (input, lexeme, Token.EOF)

    # done
    # reads an identifier
    if charClass == CharClass.LETTER:
        input, lexeme = addChar(input, lexeme)
        while True:
            c, charClass = getChar(input)
            if charClass == CharClass.LETTER or charClass == CharClass.DIGIT:
                input, lexeme = addChar(input, lexeme)
                if lexeme in lookupToken:
                    return (input, lexeme, lookupToken[lexeme])
            else:
                return (input, lexeme, Token.IDENTIFIER)

    # done 
    # reads digets 0-9
    if charClass == CharClass.DIGIT:
        input, lexeme = addChar(input, lexeme)
        while True:
            c, charClass = getChar(input)
            if charClass == CharClass.DIGIT:
                input, lexeme = addChar(input, lexeme)
            if charClass == CharClass.FLOATP:
                input, lexeme = addChar(input, lexeme)
                while True:
                    c, charClass = getChar(input)
                    if charClass == CharClass.DIGIT:
                        input, lexeme = addChar(input, lexeme)
                    else:
                        return input, lexeme, Token.FLOAT_LITERAL
            else:
                return (input, lexeme, Token.INT_LITERAL)  

    # done
    # reads oporators * / + -
    if charClass == CharClass.OPERATOR:
        input, lexeme = addChar(input, lexeme)
        if lexeme in lookupToken:
            return (input, lexeme, lookupToken[lexeme])

    # done
    # reads delimeters () {} []
    if charClass == CharClass.DELIMITER:
        input, lexeme = addChar(input, lexeme)
        return (input, lexeme, lookupToken[lexeme])

    # done
    # reads quote
    if charClass == CharClass.QUOTE:
        input, lexeme = addChar(input, lexeme)
        while True:
            c, charClass = getChar(input)
            if charClass == CharClass.QUOTE:
                input, lexeme = addChar(input, lexeme)
                return input, lexeme, Token.CHAR_LITERAL
            else:
                input, lexeme = addChar(input, lexeme)

    # done
    # reads oporators
    if charClass == CharClass.COMPARE:
        input, lexeme = addChar(input, lexeme)
        c, charClass = getChar(input)
        if c == "=":
            input, lexeme = addChar(input, lexeme)
            return input, lexeme, lookupToken[lexeme]
        else:
            return input, lexeme, lookupToken[lexeme]

    # done
    if charClass == CharClass.OTHER:
        input, lexeme = addChar(input, lexeme)
        if lexeme in lookupToken:
            return (input, lexeme, lookupToken[lexeme])

    # anything else, raises an error
    raise Exception(errorMessage(3))

# done
# parse
def parse(input):
    # TODOd: create the parse tree
    tree = Tree()
    # call parse expression
    parseProgram(input, tree)
    # return the parse tree
    return tree

# TODO
# debug
# restart correctly
# <program>       → int main ( ) { <declaration>+ <statement>+ }
def parseProgram(input, tree):
    # update the tree's root with the label
    tree.data = "<program>"

   # consume int
    input, lexeme, token = lex(input)
    if token == Token.INT_TYPE:
        tree.add(lexeme) 
    else:
        raise Exception(errorMessage(12))

    # consume main
    input, lexeme, token = lex(input)
    if token == Token.MAIN:
        tree.add(lexeme) 
    else:
        raise Exception(errorMessage(11))

    # consume {
    input, lexeme, token = lex(input)
    if token == Token.OPEN_PAR:
            tree.add(lexeme)
    else:
        raise Exception(errorMessage(10))

    # consume }
    input, lexeme, token = lex(input)
    if token == Token.CLOSE_PAR:
            tree.add(lexeme)
    else:
        raise Exception(errorMessage(9))

    # consume (
    input, lexeme, token = lex(input)
    if token == Token.OPEN_CURLY:
            tree.add(lexeme)
            # TODO the + 's
            input, lexeme, token = parseDecloration(input, tree)
            input, lexeme, token = parseStatement(input, tree)
            input, lexeme, token = lex(input)
            # consume )
            if token == Token.CLOSE_CURLY:
                tree.add(lexeme) #not working
            #this is breaking the tree parser for source 1-5 and source 13-15
            # else:
            #     raise Exception(errorMessage(7))
    else:
        raise Exception(errorMessage(8))

    return Tree

# done?
# <declaration>   → <type> <identifier> [ [ <int_literal> ] ] { , <identifier> [ [ <int_literal> ] ] } ;
def parseDecloration(input, tree):
    # create a subtree with the label <delcoration>
    subTree = Tree()
    subTree.data = "<decloration>"

    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    input, lexeme, token = parseType(input, subTree)
    input, lexeme, token = parseIdentifier(input, subTree)

    # consume [
    input, lexeme, token = lex(input)
    if token == Token.OPEN_BRACKET:
        subTree.add(lexeme)
        input, lexeme, token = parseInt_literal(input, subTree)
            # consume ]
        input, lexeme, token = lex(input)
        if token == Token.CLOSE_BRACKET:
            subTree.add(lexeme)
        else:
            raise Exception(errorMessage(13))

    while True:
        if token == Token.COMMA:
            subTree.add(lexeme)
            input, lexeme, token = parseIdentifier(input, subTree)    

            # consume [
            input, lexeme, token = lex(input)
            if token == Token.OPEN_BRACKET:
                subTree.add(lexeme)
                input, lexeme, token = parseInt_literal(input, subTree)

                # consume ]
                input, lexeme, token = lex(input)
                if token == Token.CLOSE_BRACKET:
                    subTree.add(lexeme)
                else:
                    raise Exception(errorMessage(13))
        else:
            break

    # consume [
    input, lexeme, token = lex(input)
    if token == Token.SEMICOLON:
            subTree.add(lexeme)
    # else:
    #     raise Exception(errorMessage(17))

    # TODOd: return input, lexeme, token
    return input, lexeme, token

# TODO
# How to do the or on these?
# <statement>     → <assignment> | <if> | <while> | { <statement>+ }
def parseStatement(input, tree):
    # create a subtree with the label <delcoration>
    subTree = Tree()
    subTree.data = "<decloration>"

    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)
    input, lexeme, token = lex(input)

    if token == Token.ASSIGNMENT:
        input, lexeme, token = parseAssignment(input, subTree)

    elif token == Token.IF:
        input, lexeme, token = parseif(input, subTree)

    elif token == Token.WHILE:
        input, lexeme, token = parseWhile(input, subTree)
        
    # consume {
    elif token == Token.OPEN_CURLY:
            subTree.add(lexeme)
            input, lexeme, token = parseStatement(input, subTree)

            # consume }
            input, lexeme, token = lex(input)
            if token == Token.CLOSE_CURLY:
                subTree.add(lexeme) #not working
            else:
                raise Exception(errorMessage(7))
    # source 1-5 will not work and will get stuck here aswell     
    # else:
    #     raise Exception(errorMessage(17)) # source 14-15 get stuck here incorrect

    # TODOd: return input, lexeme, token
    return input, lexeme, token

# done?
# <assignment>    → <identifier> [ [ <expression> ] ] = <expression> ;
def parseAssignment(input, tree):
    subTree = Tree()
    subTree.data = "<assignment>"

    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    input, lexeme, token = parseIdentifier(input, subTree)
 
    # consume [ optional
    input, lexeme, token = lex(input)
    if token == Token.OPEN_BRACKET:
            subTree.add(lexeme)
            input, lexeme, token = parseExpression(input, subTree)

            # consume ] 
            input, lexeme, token = lex(input)
            if token == Token.CLOSE_BRACKET:
                subTree.add(lexeme)
            else:
                raise Exception(errorMessage(13))
    # else:
    #     raise Exception(errorMessage(15))

    input, lexeme, token = lex(input)
    # consume =
    if token == Token.ASSIGNMENT:
            subTree.add(lexeme)
            input, lexeme, token = parseExpression(input, subTree)
    else:
        raise Exception(errorMessage(18))

    # consume ;
    input, lexeme, token = lex(input)
    if token == Token.SEMICOLON:
            subTree.add(lexeme)
    else:
        raise Exception(errorMessage(17))

    # TODOd: return input, lexeme, token
    return input, lexeme, token

# done
# <if>            → if ( <expression> ) <statement> [ else <statement> ]
def parseif(input, tree):
    subTree = Tree()
    subTree.data = "<if>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    # consume (
    input, lexeme, token = lex(input)
    if token == Token.OPEN_PAR:
            subTree.add(lexeme)
            input, lexeme, token = parseExpression(input, subTree)

            # consume )
            input, lexeme, token = lex(input)
            if token == Token.CLOSE_PAR:
                subTree.add(lexeme)
            else:
                raise Exception(errorMessage(9))
    else:
        raise Exception(errorMessage(10))

    input, lexeme, token = parseStatement(input, subTree)

    # maybe while? or only {} repetition
    # consume else optional
    if token == Token.ELSE:
        input, lexeme, token = parseStatement(input, subTree)

    # TODOd: return input, lexeme, token
    return input, lexeme, token

# done
# <while>         → while ( <expression> ) <statement> 
def parseWhile(input, tree):
    subTree = Tree()
    subTree.data = "<while>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    input, lexeme, token = lex(input)
    # consume while
    if token == Token.WHILE:
            subTree.add(lexeme)
    else:
        raise Exception(errorMessage(19))

    # consume (
    input, lexeme, token = lex(input)
    if token == Token.OPEN_PAR:
            subTree.add(lexeme)
            input, lexeme, token = parseExpression(input, subTree)

            # consume )
            input, lexeme, token = lex(input)
            if token == Token.CLOSE_PAR:
                subTree.add(lexeme)
            else:
                raise Exception(errorMessage(9))
    else:
        raise Exception(errorMessage(10))

    input, lexeme, token = parseStatement(input, subTree)

    # TODOd: return input, lexeme, token
    return input, lexeme, token

# done
# <expression>    → <conjunction> { || <conjunction> } 
def parseExpression(input, tree):
    subTree = Tree()
    subTree.data = "<expression>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    input, lexeme, token = parseConjunction(input, subTree)
    # parse more terms
    while True:
        input, lexeme, token = lex(input)
        # TODOd: if current token is + or - then add the lexeme to the tree and call parse term again
        if token == Token.OR:
            tree.add(lexeme)
            input, lexeme, token = parseConjunction(input, tree)

        # NOTSUREABOUTEOF??????
        elif token == Token.EOF:
            break

        # TODOd: raise an exception
        else:
            raise Exception(errorMessage(5))

    # TODOd: return input, lexeme, token
    return input, lexeme, token

# done
# <conjunction>   → <equality> { && <equality> }
def parseConjunction(input, tree):
    subTree = Tree()
    subTree.data = "<conjunction>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    input, lexeme, token = parseEquality(input, subTree)
    # parse more terms
    while True:
        input, lexeme, token = lex(input)
        # TODOd: if current token is + or - then add the lexeme to the tree and call parse term again
        if token == Token.AND:
            tree.add(lexeme)
            input, lexeme, token = parseEquality(input, tree)

        # else:
        #     raise Exception(errorMessage(5))

    # TODOd: return input, lexeme, token
    return input, lexeme, token

# done
# <equality>      → <relation> [ <eq_neq_op> <relation> ]
def parseEquality(input, tree):
    subTree = Tree()
    subTree.data = "<equality>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    input, lexeme, token = parseRelation(input, subTree)
    # parse more 
    while True:
        # TODOd: if current token is * or / then add the lexeme to the tree and call parse factor again
        if token == Token.EQUALITY or token == Token.INEQUALITY:
            subTree.add(lexeme)
            input, lexeme, token = parseRelation(input, subTree)        
        else:
            break
    
    # TODOd: return input, lexeme, token
    return input, lexeme, token


# NO IDEA HERE-----------------------------------
def parseRelation(input, tree):
    subTree = Tree()
    subTree.data = "<equality>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    input, lexeme, token = lex(input)

    # TODOd: return input, lexeme, token
    return input, lexeme, token

# done 
# maybe different error message?
def parseEq_neq_op(input, tree):
    subTree = Tree()
    subTree.data = "<eq_neq_op>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    # consume == or !=
    input, lexeme, token = lex(input)
    if token == Token.EQUALITY or token == Token.INEQUALITY :
            subTree.add(lexeme)
    else:
        raise Exception(errorMessage(5))
    
   # TODOd: return input, lexeme, token 
    return input, lexeme, token

# done
# maybe different error message
def parseRel_op(input, tree):
    subTree = Tree()
    subTree.data = "<eq_neq_op>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    # consume < or <= or > or >=
    input, lexeme, token = lex(input)
    if token == Token.LESS or token == Token.LESS_EQUAL or token == Token.GREATER or token == Token.GREATER_EQUAL:
            subTree.add(lexeme)
    else:
        raise Exception(errorMessage(5))

    # TODOd: return input, lexeme, token 
    return input, lexeme, token

# done
# <addition>      → <term> { <add_sub_op> <term> }
def parseAddition(input, tree):
    subTree = Tree()
    subTree.data = "<addition>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    input, lexeme, token = parseTerm(input, subTree)
    # parse more 
    while True:
        if token == Token.ADD or token == Token.SUBTRACT:
            subTree.add(lexeme)
            input, lexeme, token = parseTerm(input, subTree)        
        else:
            break

    # TODOd: return input, lexeme, token
    return input, lexeme, token

# done
# maybe different error message
def parseAdd_sub_op(input, tree):
    subTree = Tree()
    subTree.data = "<add_sub_op>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

  # TODOd: read a token
    # consume + or -
    input, lexeme, token = lex(input)
    if token == Token.ADD or token == Token.SUBTRACT:
            subTree.add(lexeme)
    else:
        raise Exception(errorMessage(5))
    
    # TODOd: return input, lexeme, token
    return input, lexeme, token

# done
# <term>          → <factor> { <mul_div_op> <factor> }
def parseTerm(input, tree):
    subTree = Tree()
    subTree.data = "<term>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    input, lexeme, token = parseFactor(input, subTree)
    # parse more 
    while True:
        if token == Token.MULTIPLY or token == Token.DIVIDE:
            input, lexeme, token = parseMul_div_op(input, subTree)        
            input, lexeme, token = parseFactor(input, subTree)        
        else:
            break

    # TODOd: return input, lexeme, token
    return input, lexeme, token

# done 
def parseMul_div_op(input, tree):
    subTree = Tree()
    subTree.data = "<mul_div_op>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

  # TODOd: read a token
    input, lexeme, token = lex(input)
    # consume * or /
    if token == Token.MULTIPLY or token == Token.DIVIDE:
            subTree.add(lexeme)
    else:
        raise Exception(errorMessage(5))

    # TODOd: return input, lexeme, token
    return input, lexeme, token

# done?
# <factor>        → <identifier> [ [ <expression> ] ] | <literal> | ( <expression> ) 
def parseFactor(input, tree):
    subTree = Tree()
    subTree.data = "<factor>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    input, lexeme, token = parseIdentifier(input, subTree)

    # optional
    # consume [
    input, lexeme, token = lex(input) 
    if token == Token.OPEN_BRACKET:
            subTree.add(lexeme)
            input, lexeme, token = parseExpression(input, subTree)

            # consume ]
            input, lexeme, token = lex(input)
            if token == Token.CLOSE_BRACKET:
                subTree.add(lexeme)
            else:
                raise Exception(errorMessage(13))
    else:
        raise Exception(errorMessage(15))

    # or 
    input, lexeme, token = parseLiteral(input, subTree)

    # or
    # consume ( 
    input, lexeme, token = lex(input)  
    if token == Token.OPEN_PAR:
            subTree.add(lexeme)
            input, lexeme, token = parseExpression(input, subTree)
            
            # consume )
            input, lexeme, token = lex(input)
            if token == Token.CLOSE_PAR:
                subTree.add(lexeme)
            else:
                raise Exception(errorMessage(9))
    else:
        raise Exception(errorMessage(10))

    # TODOd: return input, lexeme, token
    return input, lexeme, token

# done
# change error message
def parseType(input, tree):
    subTree = Tree()
    subTree.data = "<type>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    # consume int or
    input, lexeme, token = lex(input)
    if token == Token.INT_TYPE or token == Token.BOOL_TYPE or token == Token.FLOAT_TYPE or token == Token.CHAR_TYPE :
            subTree.add(lexeme)
    else:
        raise Exception(errorMessage(18))

    # TODOd: return input, lexeme, token 
    return input, lexeme, token

# done?
# maybe?
# dont know think I can skip the Parse letter and digit
# <identifier>    → <letter> { <letter> | <digit> }
def parseIdentifier(input, tree):
    subTree = Tree()
    subTree.data = "<identifier>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    input, lexeme, token = parseLetter(input, subTree) 

    input, lexeme, token = lex(input)
    if token == Token.IDENTIFIER:
        subTree.add(lexeme)

        # parse more Letters or DIgets
        while True:
            if token == Token.IDENTIFIER or token == Token.INT_LITERAL:
                subTree.add(lexeme)
                input, lexeme, token = parseLetter(input, subTree)
            elif token == Token.INT_LITERAL:
                input, lexeme, token = parseDigit(input, subTree)
            else:
                break

    # TODOd: return input, lexeme, token
    return input, lexeme, token

# # done?
def parseLetter(input, tree):
    subTree = Tree()
    subTree.data = "<letter>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    input, lexeme, token = lex(input)
    # consume a-z 
    # if token == Token.IDENTIFIER:
    subTree.add(lexeme)
    # else:
    #     raise Exception(errorMessage(16))
    
    # TODOd: return input, lexeme, token
    return input, lexeme, token

# done
def parseDigit(input, tree):
    subTree = Tree()
    subTree.data = "<digit>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    input, lexeme, token = lex(input)
    # consume 1-9
    if token == Token.INT_LITERAL:
        subTree.add(lexeme)
    else:
        raise Exception(errorMessage(4))
    
    # TODOd: return input, lexeme, token
    return input, lexeme, token

# done?
# # <literal>       → <int_literal> | <bool_literal> | <float_literal> | <char_literal> 
def parseLiteral(input, tree):
    subTree = Tree()
    subTree.data = "<literal>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    input, lexeme, token = lex(input)

    if token == Token.INT_LITERAL:
        input, lexeme, token = parseInt_literal(input, subTree)

    elif token == Token.FALSE or token == Token.TRUE:
        input, lexeme, token = parseBool_literal(input, subTree)

    elif token == Token.FLOAT_LITERAL:
        input, lexeme, token = parseFloat_literal(input, subTree)

    elif token == Token.CHAR_LITERAL:
        input, lexeme, token = parseChar_literal(input, subTree)

    else:
        raise Exception(errorMessage(99))

    # TODOd: return input, lexeme, token
    return input, lexeme, token

# done?
# <int_literal>   → <digit> { <digit> } 
def parseInt_literal(input, tree):
    subTree = Tree()
    subTree.data = "<int_literal>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    input, lexeme, token = lex(input)
    if token == Token.INT_LITERAL:
        subTree.add(lexeme)

        # parse more Letters or DIgets
        while True:
            if token == Token.INT_LITERAL:
                subTree.add(lexeme)
                #input, lexeme, token = parseLetter(input, subTree)
            else:
                break
        else:
            raise Exception(errorMessage(16))

    # TODOd: return input, lexeme, token
    return input, lexeme, token

# done
# check error message add tests
def parseBool_literal(input, tree):
    subTree = Tree()
    subTree.data = "<bool_literal>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    # consume true or false
    input, lexeme, token = lex(input)
    if token == Token.TRUE or token == Token.FALSE:
        subTree.add(lexeme)
    else:
        raise Exception(errorMessage(16))

    # TODOd: return input, lexeme, token
    return input, lexeme, token

# done
# check error message
# <float_literal> → <int_literal> . <int_literal>
def parseFloat_literal(input, tree):
    subTree = Tree()
    subTree.data = "<float_literal>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)
    #input, lexeme, token = parseInt_literal(input, subTree)

    input, lexeme, token = lex(input)
    # consume . 
    if token == Token.FLOAT_LITERAL:
        subTree.add(lexeme)
    else: # FIX ERROR 
        raise Exception(errorMessage(4))

    #input, lexeme, token = parseInt_literal(input, subTree)
    # TODOd: return input, lexeme, token
    return input, lexeme, token

# done
# <char_literal>  → ' <letter> '
def parseChar_literal(input, tree):
    subTree = Tree()
    subTree.data = "<char_literal>"
    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    # consume '
    input, lexeme, token = lex(input)
    if token == Token.CHAR_LITERAL:
        subTree.add(lexeme)

        # consume letter
        input, lexeme, token = lex(input)
        if token == Token.IDENTIFIER:
            subTree.add(lexeme)
            # consume ' 
            input, lexeme, token = lex(input)
            if token == Token.CHAR_LITERAL:
                subTree.add(lexeme)
            else: # FIX ERROR MESAGE
                raise Exception(errorMessage(16))
        else: # FIX ERROR MESAGE
            raise Exception(errorMessage(5))
    else: # FIX ERROR MESAGE
        raise Exception(errorMessage(16))
    
    # TODOd: return input, lexeme, token
    return input, lexeme, token

# main
if __name__ == "__main__":

    # checks if source file was passed and if it exists
    if len(sys.argv) != 2:
        raise ValueError("Missing source file")
    source = open(sys.argv[1], "rt")
    if not source:
        raise IOError("Couldn't open source file")
    input = source.read()
    source.close()
    output = []

    # calls the parser function
    tree = parse(input)

    # prints the tree if the code is syntactically correct
    if tree:
        print("Input is syntactically correct!")
        print("Parse Tree:")
        tree.print()
    else:
        # prints error message otherwise
        print("Code has syntax errors!")
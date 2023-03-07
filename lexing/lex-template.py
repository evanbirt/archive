# CS3210 - Principles of Programming Languages - Spring 2020
# A Lexical Analyzer for expressions
# Template provided by Dr. Thyago Mota

from enum import Enum
import sys

# all char classes
class CharClass(Enum):
    EOF        = 1
    LETTER     = 2
    IDENTIFIER = 3
    BLANK      = 4
    OTHER      = 5

# reads the next char from input and returns its class EOF,letter,idendifier,blank,other
def getChar(input):
    if len(input) == 0:
        return (None, CharClass.EOF)
    c = input[0].lower()
    if c.isalpha():
        return (c, CharClass.LETTER)
    if c in ['$']:
        return(c, CharClass.IDENTIFIER)
    if c in [' ', '\n', '\t']:
        return (c, CharClass.BLANK)
    return (c, CharClass.OTHER)

# calls getChar and getChar until it returns a non-blank
def getNonBlank(input):
    ignore = ""
    while True:
        c, charClass = getChar(input)
        if charClass == CharClass.BLANK:
            input, ignore = addChar(input, ignore)
        else:
            return input

# adds the next char from input to lexeme, advancing the input by one char
def addChar(input, lexeme):
    if len(input) > 0:
        lexeme += input[0]
        input = input[1:]
    return (input, lexeme)

# all tokens
class Token(Enum):
    DECLARE    = 1
    IDENTIFIER = 2
    REAL       = 3
    COMPLEX    = 4
    FIXED      = 5
    FLOATING   = 6
    SINGLE     = 7
    DOUBLE     = 8
    BINARY     = 9
    DECIMAL    = 10

lookup = {
    "declare"   : Token.DECLARE,
    "real"      : Token.REAL,
    "complex"   : Token.COMPLEX,
    "fixed"     : Token.FIXED,
    "floating"  : Token.FLOATING,
    "single"    : Token.SINGLE,
    "double"    : Token.DOUBLE,
    "binary"    : Token.BINARY,
    "decimal"   : Token.DECIMAL
}

# returns the next (lexeme, token) pair or None if EOF is reached. EOF, Letter, Identifier
def lex(input):
    input = getNonBlank(input)

    c, charClass = getChar(input)
    lexeme = ""

    # check EOF first
    if charClass == CharClass.EOF:
        return (input, None, None)

    # TODOd: read a letter followed by letters
    if charClass == CharClass.LETTER:
        input, lexeme = addChar(input, lexeme)

        while True:
            c, charClass = getChar(input)
            if charClass == CharClass.LETTER:
                input, lexeme = addChar(input, lexeme)
                if lexeme in lookup:
                    return (input, lexeme, lookup[lexeme])
            else:
                return (input, lexeme, Token.IDENTIFIER)

    # TODOd: catch symbol
    if charClass == CharClass.IDENTIFIER:

        input, lexeme = addChar(input, lexeme)
        while True:
                c, charClass = getChar(input)
                if charClass == CharClass.LETTER:
                    input, lexeme = addChar(input, lexeme)
                else:
                    return (input, lexeme, Token.IDENTIFIER)

    # TODOd: anything else, raise an exception
    raise Exception("Exception: Lexical Analyzer Error: unrecognized symbol found!")

# main
if __name__ == "__main__":
    # checks if source file was passed and if it exists
    if len(sys.argv) != 2:
        raise ValueError("Missing source file")

    with open(sys.argv[1]) as source:
        if '$' in source.read():
            source = open(sys.argv[1], "rt")
        else:
            print("Exception: Lexical Analyzer Error: unrecognized symbol found!")
            sys.exit(1) # Suggestion from Tyler to add this line

    if not source:
        raise IOError("Couldn't open source file")

    input = source.read()
    source.close()
    output = []
    #print("exit message error here")
    #sys.exit(1)

    # main loop
    while True:
        input, lexeme, token = lex(input)
        if lexeme == None:
            break
        output.append((lexeme, token))

    # prints the output
    for (lexeme, token) in output:
        print(lexeme, token)
import re


def Counter():
    """
    The Counter method keeps track of the program counter.
    :return:
    """
    i = 0
    while True:
        yield i
        i += 1


class Lexer:
    """
    The Lexer class analyzes Clite tokens
    """

    # Constants that represent token classifiers
    cnt = Counter()

    # operators
    PLUS = next(cnt)
    MINUS = next(cnt)
    TIMES = next(cnt)
    EXPONENTIAL = next(cnt)
    DIV = next(cnt)
    MOD = next(cnt)
    COMMENT = next(cnt)
    NOT = next(cnt)
    AND = next(cnt)
    OR = next(cnt)
    EQEQ = next(cnt)
    NOTEQ = next(cnt)
    STRINGLIT = next(cnt)
    MAIN = next(cnt)

    LESSEQ = next(cnt)
    LESS = next(cnt)

    GREATEQ = next(cnt)
    GREAT = next(cnt)

    EQ = next(cnt)

    # literals
    ID = next(cnt)
    INTLIT = next(cnt)
    FLOATLIT = next(cnt)

    # keywords
    KWDIF = next(cnt)
    KWDPRINT = next(cnt)
    KWDBOOL = next(cnt)
    KWDELSE = next(cnt)
    KWDFALSE = next(cnt)
    KWDTRUE = next(cnt)
    KWDFLOAT = next(cnt)
    KWDINT = next(cnt)
    KWDWHILE = next(cnt)

    # punctuation
    SEMI = next(cnt)
    OPENBRA = next(cnt)
    CLOSEDBRA = next(cnt)
    OPENP = next(cnt)
    CLOSEDP = next(cnt)
    COMMA = next(cnt)
    OPENB = next(cnt)
    CLOSEDB = next(cnt)

    # errors
    FILENOTFOUND = next(cnt)
    ILLEGALTOKEN = next(cnt)
    EOF          = next(cnt)

    # precompile the regex of patterns
    # to split tokens on.

    split_patt = re.compile(
        """
        \s   |    # whitespace
        (\|\|)|    # operator || (logical or) 
        (\/\/) |  # Comments
        (&&) |    # operator && (logical and)
        (==) |    # operator ==
        (!=) |    # operator !=
        (>=) |    # operator >=
        (\>)  |    # operator > 
        (<=) |    # operator <= 
        (\<)  |    # operator < 
        (=)  |    # operator =
        (\+) |    # operator +
        (-)  |    # operator -
        (\*\*) | 
        (\*) |    # operator *
        (/)  |    # operator / 
        (%)  |    # operator %
        (!)  |    # operator !
        #end of operators, start of punctuation
        (;)   |    # punctuation ;
        (\,)  |    # punctuation ,
        (\[)  |
        (\]) |
        (\{)  |    # punctuation {
        (\})  |    # punctuation }
        ( \( ) |    # punctuation (
        ( \) )   # punctuation )
        """,
        re.VERBOSE
    )

    # regular expression (regex) for an identifier
    id_patt = re.compile("^[a-zA-Z_\"][a-zA-Z0-9_\"]*$")
    intlit_patt = re.compile("^[0-9]*$")
    floatlit_patt = re.compile("^[0-9\-][0-9.]*$")

    # token dictionary
    td = {
        # operators
        '+': PLUS,
        '-': MINUS,
        '*': TIMES,
        '**': EXPONENTIAL,
        '//': COMMENT,
        '/': DIV,
        '%': MOD,
        '!': NOT,

        '&&': AND,
        '||': OR,

        '==': EQEQ,
        '!=': NOTEQ,

        '<': LESS,
        '<=': LESSEQ,
        '>': GREAT,
        '>=': GREATEQ,

        '=': EQ,

        # punctuation
        ',': COMMA,
        '[': OPENBRA,
        ']': CLOSEDBRA,
        '{': OPENB,
        '}': CLOSEDB,
        '(': OPENP,
        ')': CLOSEDP,
        ';': SEMI,

    }

    def token_generator(self, filename):
        try:
            file = open(filename)
        except IOError:
            yield (Lexer.FILENOTFOUND, filename)

        line_counter = 1
        for line in file:
            tokens = Lexer.split_patt.split(line)
            tokens = [t for t in tokens if t]

            for t in tokens:

                if t == '//' or t == '#':
                    break;

                elif t in Lexer.td:
                    yield (Lexer.td[t], t, "Line Number: " + str(line_counter))

                # Handle keywords
                elif Lexer.id_patt.search(t):
                    if t == 'if': # use dictionary
                        yield (Lexer.KWDIF, 'if', "Line Number: " + str(line_counter))
                    elif t == 'print':
                        yield (Lexer.KWDPRINT, 'print', "Line Number: " + str(line_counter))
                    elif t == 'bool':
                        yield (Lexer.KWDBOOL, 'bool', "Line Number: " + str(line_counter))
                    elif t == 'else':
                        yield (Lexer.KWDELSE, 'else', "Line Number: " + str(line_counter))
                    elif t == 'false':
                        yield (Lexer.KWDFALSE, 'false', "Line Number: " + str(line_counter))
                    elif t == 'true':
                        yield (Lexer.KWDTRUE, 'true', "Line Number: " + str(line_counter))
                    elif t == 'float':
                        yield (Lexer.KWDFLOAT, 'float', "Line Number: " + str(line_counter))
                    elif t == 'int':
                        yield (Lexer.KWDINT, 'int', "Line Number: " + str(line_counter))
                    elif t == 'while':
                        yield (Lexer.KWDWHILE, 'while', "Line Number: " + str(line_counter))
                    elif t == 'main':
                        yield (Lexer.MAIN, 'main', "Line Number: " + str(line_counter))
                    else:
                        yield (Lexer.ID, t, "Line Number: " + str(line_counter))

                # Int literal search
                elif Lexer.intlit_patt.search(t):  # check for integer literal
                    yield (Lexer.INTLIT, t, "Line Number: " + str(line_counter))

                # Float literal search
                elif Lexer.floatlit_patt.search(t):
                    if t.count('.') >= 2:
                        yield (Lexer.ILLEGALTOKEN, t, "Line Number: " + str(line_counter))
                    else:
                        yield (Lexer.FLOATLIT, t, "Line Number: " + str(line_counter))

                # If no match, yield an error
                else:
                    yield (Lexer.ILLEGALTOKEN, t, "Error on Line Number: " + str(line_counter))

            line_counter += 1

        # Yield end of file
        yield (Lexer.EOF, "End Of File", "Line Number:" + str(line_counter))


if __name__ == "__main__":

    lex = Lexer()
    tg = lex.token_generator('lexertest.c')

    # Format for how proffessor wants it
    print("Token     Name    Line Number \n"
          "-----------------------------")

    while True:
        try:
            tok = next(tg)
            print(tok)
        except StopIteration:
            break







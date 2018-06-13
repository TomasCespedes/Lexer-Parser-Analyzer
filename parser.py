import ast
import lexer

# Uncomment below to run file from terminal
# import sys

"""
Addition → Term  {AddOp Term}
Term → Factor {MulOp Factor}
Factor → [UnaryOp] Primary
UnaryOp →   ­ | !
Primary → id | intlit | floatlit | ( Addition )
AddOp -> + | -
MulOp -> * | / | %
"""


class Parser:

    def __init__(self, filename):

        lex = lexer.Lexer()
        self.tokens = lex.token_generator(filename)
        self.currtok = next(self.tokens)

    def parse(self):
        return self.program()

    def program(self):
        """
         Program   ⇒  int  main ( ) { Declarations Statements }
        :return:
        """

        # Check if the current token is a keyword Int
        if self.currtok[0] == lexer.Lexer.KWDINT:
            self.currtok = next(self.tokens)

            # Check if the current token is "main"
            if self.currtok[0] == lexer.Lexer.MAIN:
                self.currtok = next(self.tokens)

                # Check if the current token is an open parenthesis
                if self.currtok[0] == lexer.Lexer.OPENP:
                    self.currtok = next(self.tokens)

                    # Check if the current token is a closed parenthesis
                    if self.currtok[0] == lexer.Lexer.CLOSEDP:
                        self.currtok = next(self.tokens)

                        # Check if the current token is an open bracket
                        if self.currtok[0] == lexer.Lexer.OPENB:
                            self.currtok = next(self.tokens)

                            # Run the declation and statements methods on
                            # the entire program
                            decls = self.declarations()
                            stmts = self.statements()

                            # Check if the current token is a closed bracket
                            if self.currtok[0] == lexer.Lexer.CLOSEDB:
                                return ast.Program(decls, stmts)

                            # Closed bracket not found, throw syntax error
                            else:
                                raise CliteSyntaxError("Expected curly bracket on line " + self.currtok[2])

                        # Open bracket not found, throw syntax error
                        else:
                            raise CliteSyntaxError("Expected curly bracket on line " + self.currtok[2])

                    # Closed parenthesis not found, throw syntax error
                    else:
                        raise CliteSyntaxError("Expected Parenthesis on line " + self.currtok[2])

                # Open parenthesis not found, throw syntax error
                else:
                    raise CliteSyntaxError("Expected Parenthesis on line " + self.currtok[2])

            # "main" not found, throw syntax error
            else:
                raise CliteSyntaxError("Expected main on line " + self.currtok[2])

        # keyword int not found, throw syntax error
        else:
            raise CliteSyntaxError("Expected int on line " + self.currtok[2])

    def declarations(self):
        """
        Declarations    ⇒  { Declaration }
        :return:
        """

        # Create a dictionary for declarations
        # Similar to statements
        decls = dict()

        # Check if the current token is a
        # keyword int, keyword float, or keyword bool
        while self.currtok[0] in [lexer.Lexer.KWDINT, lexer.Lexer.KWDFLOAT,
                                  lexer.Lexer.KWDBOOL]:

            declaration = self.declaration()
            decls[declaration.id] = declaration.type

        return decls

    def declaration(self):
        """
        Declaration     ⇒  Type  Identifier  ;
        :return:
        """

        # Just follow the language above
        temp = self.type()
        self.currtok = next(self.tokens)

        return temp

    def type(self):
        """  Type            ⇒  int | bool | float"""

        # Check to see if current token is
        # a keyword int, keyword bool, or keyword Float
        if self.currtok[0] in [lexer.Lexer.KWDINT, lexer.Lexer.KWDBOOL, lexer.Lexer.KWDFLOAT]:
            temptype = self.currtok[1]
            self.currtok = next(self.tokens)

            tempid = self.currtok[1]
            self.currtok = next(self.tokens)

            return ast.Declaration(temptype, tempid)

    def statements(self):
        """
        Statements      ⇒  { Statement }
        :return:
        """

        # Create a dictionary for statements
        statements = []

        # Check to see if the current token is a Semi-Colon, Open bracket,
        # Identifier, keyword If, keyword While, or keyword Print
        while self.currtok[0] in [lexer.Lexer.SEMI, lexer.Lexer.OPENB, lexer.Lexer.ID,
                                  lexer.Lexer.KWDIF, lexer.Lexer.KWDWHILE, lexer.Lexer.KWDPRINT]:
            tempstatment = self.statement()

            # Add the temporary statement to the
            # dictionary of statements
            statements.append(tempstatment)

        return statements

    def statement(self):
        """
         ; | Block | Assignment | IfStatement
                       | WhileStatement | PrintStatement
        :return:
        """

        # Check to see if current token is a Semi colon
        if self.currtok[0] == lexer.Lexer.SEMI:
            tempsemi = self.currtok[1]
            return ast.Semicolon(tempsemi)

        # Check to see if current token is an opening bracket
        # Because that is the first token expected in a Block call
        elif self.currtok[0] == lexer.Lexer.OPENB:
            return self.block()

        # Check to see if current token is an Identifier
        elif self.currtok[0] == lexer.Lexer.ID:
            return self.assignment()

        # Check to see if current token is a keyword If
        elif self.currtok[0] == lexer.Lexer.KWDIF:
            return self.ifstatement()

        # Check to see if current token is a keyword While
        elif self.currtok[0] == lexer.Lexer.KWDWHILE:
            return self.whilestatement()

        # Check to see if current token is a keyword Print
        elif self.currtok[0] == lexer.Lexer.KWDPRINT:
            return self.printstatement()

        # No tokens match, so throw syntax error
        else:
            raise CliteSyntaxError("Unexpected token")

    def block(self):
        """
        Block           ⇒  { Statements }
        :return:
        """

        # Check to see if current token is an opening Bracket
        if self.currtok[0] == lexer.Lexer.OPENB:
            self.currtok = next(self.tokens)
            tree = self.statements()

            # Check to see if current token is a closing Bracket
            if self.currtok[0] == lexer.Lexer.CLOSEDB:
                self.currtok = next(self.tokens)
                return tree

            # If it is not a closing bracket, throw a syntax error
            elif self.currtok[0] != lexer.Lexer.CLOSEDB:
                raise CliteSyntaxError("Curly Bracket expected on line " + str(self.currtok[2]))

        # If it is not an opening bracket, throw a syntax error
        elif self.currtok[0] != lexer.Lexer.OPENB:
            raise CliteSyntaxError("Curly Bracket expected on line " + str(self.currtok[2]))

    def assignment(self):
        """
        Assignment  ⇒  Identifier = Expression ;
        :return:
        """

        left_tree = self.currtok

        # Check to see if current token is an Identifier
        if self.currtok[0] == lexer.Lexer.ID:
            self.currtok = next(self.tokens)

            # If next token is not equal to "=", throw a syntax error
            if self.currtok[0] != lexer.Lexer.EQ:
                raise CliteSyntaxError("Equals is expected on line " + str(self.currtok[2]))

        tempo = self.currtok[1]
        self.currtok = next(self.tokens)

        right_tree = self.expression()

        # Check to see if current token is a semi colon
        if self.currtok[0] == lexer.Lexer.SEMI:
            self.currtok = next(self.tokens)

        # If it is not a semi colon, throw a syntax error
        elif self.currtok[0] != lexer.Lexer.SEMI:
            raise CliteSyntaxError("Semi-colon is expected on line " + str(self.currtok[2]))

        t = ast.AssignStmt(left_tree[1], right_tree, tempo)
        return t

    def ifstatement(self):
        """
          IfStatement     ⇒  if ( Expression ) Statement [ else Statement ]
        :return:
        """

        # Check for a keyword If
        if self.currtok[0] == lexer.Lexer.KWDIF:
            self.currtok = next(self.tokens)

            # Check for opening parenthesis
            if self.currtok[0] == lexer.Lexer.OPENP:
                self.currtok = next(self.tokens)

                left_tree = self.expression()

                # Check for a closing parenthesis
                if self.currtok[0] == lexer.Lexer.CLOSEDP:
                    self.currtok = next(self.tokens)

                    right_tree = self.statement()

                    # Check for a keyword Else
                    if self.currtok[0] == lexer.Lexer.KWDELSE:
                        left_tree1 = self.currtok[1]
                        self.currtok = next(self.tokens)

                        right_tree1 = self.statement()

                        tree = ast.IfStatement(left_tree, right_tree, left_tree1, right_tree1)

                        return tree

                    tree = ast.IfStatement2(left_tree, right_tree)
                    return tree

                # If there is no closing parenthesis, throw syntax error
                elif self.currtok[0] != lexer.Lexer.CLOSEDP:
                    raise CliteSyntaxError("Parenthesis expected on line " + str(self.currtok[2]))

            # If there is no opening parenthesis, throw syntax error
            elif self.currtok[0] != lexer.Lexer.OPENP:
                raise CliteSyntaxError("Parenthesis expected on line " + str(self.currtok[2]))

    def whilestatement(self):

        """
        WhileStatement  ⇒  while ( Expression ) Statement
        :return:
        """

        # Check if the current token is a keyword While
        if self.currtok[0] == lexer.Lexer.KWDWHILE:
            self.currtok = next(self.tokens)

            # Check for an open parenthesis
            if self.currtok[0] == lexer.Lexer.OPENP:
                self.currtok = next(self.tokens)

                left_tree = self.expression()

                # Check for a closed parenthesis
                if self.currtok[0] == lexer.Lexer.CLOSEDP:
                    self.currtok = next(self.tokens)

                    right_tree = self.statement()
                    left_tree = ast.WhileStatement(left_tree, right_tree)

                    return left_tree

                # If there is no closed parenthesis, throw syntax error
                elif self.currtok[0] != lexer.Lexer.CLOSEDP:
                    raise CliteSyntaxError("Parenthesis expected on line " + str(self.currtok[2]))

            # If there is no opening parenthesis, throw syntax error
            elif self.currtok[0] != lexer.Lexer.OPENP:
                raise CliteSyntaxError("Parenthesis expected on line " + str(self.currtok[2]))

    def printstatement(self):
        """
        PrintStatement  ⇒  print( Expression ) ;
        :return:
        """

        # Check if current token is a
        # keyword Print
        if self.currtok[0] == lexer.Lexer.KWDPRINT:
            self.currtok = next(self.tokens)

            # Check if current token is an open parenthesis
            if self.currtok[0] == lexer.Lexer.OPENP:
                self.currtok = next(self.tokens)

                tree = self.expression()
                temp = ast.PrintStatement(tree)

                # Check if current token is an closed parenthesis
                if self.currtok[0] == lexer.Lexer.CLOSEDP:
                    self.currtok = next(self.tokens)

                    # Check to see if there is a semi colon after statement
                    if self.currtok[0] == lexer.Lexer.SEMI:
                        self.currtok = next(self.tokens)

                    # If not, throw syntax error
                    else:
                        raise CliteSyntaxError("Semi colon expected on line " + str(self.currtok[2]))

                # If no closed parenthesis, throw syntax error
                elif self.currtok[0] != lexer.Lexer.CLOSEDP:
                    raise CliteSyntaxError("Parenthesis expected on line " + str(self.currtok[2]))

                return temp

            # If no open parenthesis, throw syntax error
            elif self.currtok[0] != lexer.Lexer.OPENP:
                raise CliteSyntaxError("Parenthesis expected on line " + str(self.currtok[2]))

        return self.expression()

    def expression(self):
        """
        Expression      ⇒  Conjunction { || Conjunction }
        :return:
        """
        left_tree = self.conjuction()

        # Run this while the current token is
        # equal to "||" aka Or
        while self.currtok[0] == lexer.Lexer.OR:
            tempor = self.currtok[1]
            self.currtok = next(self.tokens)
            right_tree = self.conjuction()
            left_tree = ast.BinaryExpr(left_tree, right_tree, tempor)

        return left_tree

    def conjuction(self):
        """
        Conjunction     ⇒  Equality { && Equality }
        :return:
        """
        left_tree = self.equality()

        # Run this while the current token is equal
        # To "&&" aka and
        while self.currtok[0] == lexer.Lexer.AND:
            tempand = self.currtok[1]
            self.currtok = next(self.tokens)
            right_tree = self.equality()
            left_tree = ast.BinaryExpr(left_tree, right_tree, tempand)

        return left_tree

    def equality(self):
        """
        Equality  ⇒  Relation [ EquOp Relation ]
        :return:
        """
        left_tree = self.relation()

        # Check if the current token is either
        # "==" or "!="
        if self.currtok[0] in [lexer.Lexer.EQEQ, lexer.Lexer.NOTEQ]:
            tmpexpr = self.currtok[1]
            self.currtok = next(self.tokens)
            right_tree = self.relation()
            left_tree = ast.BinaryExpr(left_tree, right_tree, tmpexpr)

        return left_tree

    def relation(self):
        """
        Relation  ⇒  Addition [ RelOp Addition ]
        :return:
        """
        left_tree = self.addition()

        # Check if the current token is either a
        # less than, less than or equal to, greater than, or
        # greater than or equal to
        if self.currtok[0] in [lexer.Lexer.LESS, lexer.Lexer.LESSEQ, lexer.Lexer.GREAT, lexer.Lexer.GREATEQ]:
            tmp = self.currtok[1]
            self.currtok = next(self.tokens)
            right_tree = self.addition()
            left_tree = ast.BinaryExpr(left_tree, right_tree, tmp)

        return left_tree

    def addition(self):
        """
        Addition → Term  {AddOp Term}
        :return: BinaryPlusExpr
        """

        left_tree = self.term()

        # Run this while the current token is either
        # a plus or a minus
        while self.currtok[0] in [lexer.Lexer.PLUS, lexer.Lexer.MINUS]:
            tmp = self.currtok[1]
            self.currtok = next(self.tokens)
            right_tree = self.term()
            left_tree = ast.BinaryExpr(left_tree, right_tree, tmp)

        return left_tree

    def term(self):
        """
        Term → Factor {MulOp Factor}
        :return:
        """
        left_tree = self.factor()

        # Run this while the current token is a
        # times, division, mod, or exponential
        while self.currtok[0] in [lexer.Lexer.TIMES, lexer.Lexer.DIV, lexer.Lexer.MOD,
                                  lexer.Lexer.EXPONENTIAL]:
            tmp = self.currtok[1]
            self.currtok = next(self.tokens)
            right_tree = self.factor()
            left_tree = ast.BinaryExpr(left_tree, right_tree, tmp)

        return left_tree

    def factor(self):
        """
        Factor → [UnaryOp] Primary
        :return:
        """

        # Check if the token is either a minus or a "not" aka an UnaryOp
        if self.currtok[0] in [lexer.Lexer.MINUS, lexer.Lexer.NOT]:
            tmp = self.currtok[1]
            self.currtok = next(self.tokens)
            tree = self.primary()
            return ast.UnaryExpr(tmp, tree)

        # If not, call primary method
        else:
            return self.primary()

    def primary(self):
        """
        Primary → id | intlit | floatlit | ( Addition ) | True | False
        :return:
        """

        # Check if token is an ID
        if self.currtok[0] == lexer.Lexer.ID:
            tmpid = self.currtok[1]
            self.currtok = next(self.tokens)
            t = ast.IdExpr(tmpid)
            return t

        # Check if token is a Integer Literal
        elif self.currtok[0] == lexer.Lexer.INTLIT:
            tmpintlit = self.currtok[1]
            self.currtok = next(self.tokens)
            p = ast.IntLitExpr(tmpintlit)
            return p

        # Check if token is a Float Literal
        elif self.currtok[0] == lexer.Lexer.FLOATLIT:
            tmpfloatlit = self.currtok[1]
            self.currtok = next(self.tokens)
            q = ast.FloatLitExpr(tmpfloatlit)
            return q

        # Check if token is equal to '('
        elif self.currtok[0] == lexer.Lexer.OPENP:
            self.currtok = next(self.tokens)
            tree = self.addition()

            # Check if token is equal to ')'
            if self.currtok[0] == lexer.Lexer.CLOSEDP:
                self.currtok = next(self.tokens)
                return tree
            else:
                raise CliteSyntaxError("Expected right parentheses on line " + str(self.currtok[0]))

        # Check if token is a keyword True
        elif self.currtok[0] == lexer.Lexer.KWDTRUE:
            tmptrue = self.currtok[1]
            self.currtok = next(self.tokens)
            tr = ast.BoolExpr(tmptrue)
            return tr

        # Check if token is a keyword False
        elif self.currtok[0] == lexer.Lexer.KWDFALSE:
            tmpfalse = self.currtok[1]
            self.currtok = next(self.tokens)
            fa = ast.BoolExpr(tmpfalse)
            return fa

        # No tokens match so raise an error
        else:
            raise CliteSyntaxError("Unexpected token")


class CliteSyntaxError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


if __name__ == "__main__":

    # Uncomment below to run file from
    # terminal and comment out the line below that

    # parser = Parser(sys.argv[1])

    parser = Parser("test.c")

    tree = parser.parse()
    print(tree)

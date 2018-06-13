import lexer
# Program is a singleton class
# stmts and dcels could be class data and not
# instance data


# Initalize declarations and statements
class Program:
    def __init__(self, decls, stmts):
        self.decls = decls
        self.stmts = stmts

    def __str__(self):
        declstring = ""

        # Formatting for lexer printing
        for decl in self.decls:
            if self.decls[decl] == lexer.Lexer.KWDINT:
                declstring += '\t' + "int "
            elif self.decls[decl] == lexer.Lexer.KWDFLOAT:
                declstring += '\t' + "float "
            elif self.decls[decl] == lexer.Lexer.KWDBOOL:
                declstring += '\t' + "bool "

            declstring += "\t" + self.decls[decl] + " " + decl + ';\n'

        stmtstring = ""
        for stmt in self.stmts:

            stmtstring += '\t' + str(stmt) + "\n"

        return "int main () { \n" + declstring + stmtstring + "}"


class Declaration:
    def __init__(self, type, id):
        self.type = type
        self.id = id

    def __str__(self):
        return "({0} {1}{2})".format(str(self.type), str(self.id), str(";"))

    def __repr__(self):
        return "Declaration({0}, {1},{2}".format(repr(self.type),
                                                 repr(self.id),
                                                 ";")


class Semicolon:
    def __init__(self, semi):
        self.semi = semi

    def __str__(self):
        return "({0})".format(str(self.semi))

    def __repr__(self):
        return "Semicolon({0})".format(repr(self.semi))


class AssignStmt:
    def __init__(self, decl, expr, equals):
        self.decl = decl
        self.expr = expr
        self.equals = equals

    def __str__(self):
        return "{0} {1} {2};".format(str(self.decl), str(self.equals), str(self.expr))

    def __repr__(self):
            return '\t' + '\t' '{0} {1} {2}\n'.format(
              self.decl, self.equals, self.expr
            )


class IfStatement:
    def __init__(self, expr, statement, expr1, statement1):
        self.expr = expr
        self.statement = statement
        self.expr1 = expr1
        self.statement1 = statement1

    def __str__(self):
        return "if" + "({0} \n {1} \n {2} \n {3})".format(str(self.expr), str(self.statement),
                                                          str(self.expr1), str(self.statement1))

    def __repr__(self):
        return "if" + "IfStatement({0} , {1}, {2}, {3})".format(
            repr(self.expr), repr(self.statement), repr(self.expr1), repr(self.statement1)
        )


class IfStatement2:
    def __init__(self, expr, statement):
        self.expr = expr
        self.statement = statement

    def __str__(self):
        return "if" + "({0} {1})".format(self.expr, self.statement)

    def __repr__(self):
        return '\t' + "if" + "{0} \n \t \t {1}\n".format(str(self.expr), str(self.statement))


class WhileStatement:
    def __init__(self, expr, statement):
        self.expr = expr
        self.statement = statement
        self.opens = '{'
        self.closes = '}'

    def __str__(self):
        return "while" + "{0} \n \t {1} \n {2} \n \t {3}".format(str(self.expr), str(self.opens),
                                                      str(self.statement), str(self.closes))

    def __repr__(self):
        return "while" + "WhileStatement({0} , {1}, {2}, {3})".format(
            repr(self.expr), repr(self.opens), repr(self.statement), repr(self.closes)
        )


class PrintStatement:
    def __init__(self, statement):
        self.statement = statement

    def __str__(self):
        return "print" + "{0};".format(str(self.statement))

    def __repr__(self):
        return "print" + "PrintStatement({0})".format(
            repr(self.statement)
        )


"""
Abstract Syntax representaiotn of Clite programs
"""


class IdExpr:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class IntLitExpr:

    def __init__(self, intvalue):
        self.intvalue = intvalue

    def __str__(self):
        return self.intvalue


class FloatLitExpr:

    def __init__(self, floatvalue):
        self.floatvalue = floatvalue

    def __str__(self):
        return self.floatvalue


class BinaryExpr:

    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        return "({0} {1} {2})".format(str(self.left),
                                      self.op,
                                      str(self.right))

    def __repr__(self):
        return "BinaryExpr({0}, {1})".format(
            repr(self.left), repr(self.right)
        )

    def eval(self):
        if self.op == "+":
            return eval(self.left) + eval(self.right)
        elif self.op == "-":
            return eval(self.left) - eval(self.right)
        elif self.op == "**":
            return eval(self.left) ** eval(self.right)
        elif self.op == "*":
            return eval(self.left) * eval(self.right)
        elif self.op == "/":
            return eval(self.left) / eval(self.right)


class UnaryExpr:

    def __init__(self, expr, kind):
        self.expr = expr
        self.kind = kind

    def __repr__(self):
        return "UnaryExpr({0}, {1})".format(
            self.kind, repr(self.expr)
        )

    def __str__(self):
        return "({0}{1})".format(str(self.expr), self.kind)

    def eval(self):
        return eval(self.expr)


class BoolExpr:
    def __init__(self, case):
        self.case = case

    def __str__(self):
        return self.case


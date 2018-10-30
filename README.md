# Lexer-Parser-Analyzer
Lexer and Parser program was a 2 part program that was assigned as a project during my Programming Languages class.
CLite is our simplified programming language that looks a little like C and Java. In this assignment we completed the lexical analyzer (lexer) for CLite.

These programs were written using PyCharm. I have uploaded what I completed during the school year but since we did not use GitHub for the class there is no step by step commit available. 
The Lexer was Part 1 of the assignment. In order to test the lexer I used the lexertest.c file that is available in the repository.
The Parser was Part 2 of the assignment which builds upon Part 1. In order to test the Parser, I ran it using the test.c file that is also available within the repository. 

The Language that we had to follow for Part 2 is below.
  Program         ⇒  int  main ( ) { Declarations Statements }
  Declarations    ⇒  { Declaration }
  Declaration     ⇒  Type  Identifier  ;
  Type            ⇒  int | bool | float
  Statements      ⇒  { Statement }
  Statement       ⇒  ; | Block | Assignment | IfStatement 
                       | WhileStatement | PrintStatement
  Block           ⇒  { Statements }
  Assignment      ⇒  Identifier = Expression ;
  IfStatement     ⇒  if ( Expression ) Statement [ else Statement ]
  WhileStatement  ⇒  while ( Expression ) Statement 
  PrintStatement  ⇒  print( Expression ) ;  
  Expression      ⇒  Conjunction { || Conjunction }
  Conjunction     ⇒  Equality { && Equality }
  Equality        ⇒  Relation [ EquOp Relation ]
  EquOp           ⇒  == | != 
  Relation        ⇒  Addition [ RelOp Addition ]
  RelOp           ⇒  < | <= | > | >= 
  Addition        ⇒  Term { AddOp Term }
  AddOp           ⇒  + | -
  Term            ⇒  Factor { MulOp Factor }
  MulOp           ⇒  * | / | %
  Factor          ⇒  [ UnaryOp ] Primary
  UnaryOp         ⇒  - | !
  Primary         ⇒  Identifier | IntLit | FloatLit | ( Expression ) | true | false

# Part 1: Running just the lexer output.
![image](https://user-images.githubusercontent.com/35609863/47688830-8450f480-dbbd-11e8-93e8-b1952449d913.png)

from antlr4 import *
from _typeshed import Incomplete
from io import StringIO as StringIO
from typing import TextIO

def serializedATN(): ...

class vba_likeLexer(Lexer):
    atn: Incomplete
    decisionsToDFA: Incomplete
    T__0: int
    T__1: int
    T__2: int
    T__3: int
    CHAR: int
    WILD_CHAR: int
    WILD_SEQ: int
    WILD_DIGIT: int
    channelNames: Incomplete
    modeNames: Incomplete
    literalNames: Incomplete
    symbolicNames: Incomplete
    ruleNames: Incomplete
    grammarFileName: str
    def __init__(self, input: Incomplete | None = None, output: TextIO = ...) -> None: ...

# Generated from vba_like.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,8,75,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,6,
        2,7,7,7,2,8,7,8,1,0,5,0,20,8,0,10,0,12,0,23,9,0,1,0,1,0,1,1,1,1,
        1,1,3,1,30,8,1,1,2,1,2,1,3,1,3,1,4,1,4,3,4,38,8,4,1,4,3,4,41,8,4,
        1,4,1,4,1,5,1,5,5,5,47,8,5,10,5,12,5,50,9,5,1,5,3,5,53,8,5,1,5,4,
        5,56,8,5,11,5,12,5,57,1,5,3,5,61,8,5,3,5,63,8,5,1,6,1,6,3,6,67,8,
        6,1,7,1,7,1,8,1,8,1,8,1,8,1,8,0,0,9,0,2,4,6,8,10,12,14,16,0,3,2,
        0,1,2,5,5,1,0,6,8,2,0,3,3,5,8,76,0,21,1,0,0,0,2,29,1,0,0,0,4,31,
        1,0,0,0,6,33,1,0,0,0,8,35,1,0,0,0,10,62,1,0,0,0,12,66,1,0,0,0,14,
        68,1,0,0,0,16,70,1,0,0,0,18,20,3,2,1,0,19,18,1,0,0,0,20,23,1,0,0,
        0,21,19,1,0,0,0,21,22,1,0,0,0,22,24,1,0,0,0,23,21,1,0,0,0,24,25,
        5,0,0,1,25,1,1,0,0,0,26,30,3,4,2,0,27,30,3,8,4,0,28,30,3,6,3,0,29,
        26,1,0,0,0,29,27,1,0,0,0,29,28,1,0,0,0,30,3,1,0,0,0,31,32,7,0,0,
        0,32,5,1,0,0,0,33,34,7,1,0,0,34,7,1,0,0,0,35,37,5,3,0,0,36,38,5,
        4,0,0,37,36,1,0,0,0,37,38,1,0,0,0,38,40,1,0,0,0,39,41,3,10,5,0,40,
        39,1,0,0,0,40,41,1,0,0,0,41,42,1,0,0,0,42,43,5,2,0,0,43,9,1,0,0,
        0,44,48,5,1,0,0,45,47,3,12,6,0,46,45,1,0,0,0,47,50,1,0,0,0,48,46,
        1,0,0,0,48,49,1,0,0,0,49,52,1,0,0,0,50,48,1,0,0,0,51,53,5,1,0,0,
        52,51,1,0,0,0,52,53,1,0,0,0,53,63,1,0,0,0,54,56,3,12,6,0,55,54,1,
        0,0,0,56,57,1,0,0,0,57,55,1,0,0,0,57,58,1,0,0,0,58,60,1,0,0,0,59,
        61,5,1,0,0,60,59,1,0,0,0,60,61,1,0,0,0,61,63,1,0,0,0,62,44,1,0,0,
        0,62,55,1,0,0,0,63,11,1,0,0,0,64,67,3,14,7,0,65,67,3,16,8,0,66,64,
        1,0,0,0,66,65,1,0,0,0,67,13,1,0,0,0,68,69,7,2,0,0,69,15,1,0,0,0,
        70,71,3,14,7,0,71,72,5,1,0,0,72,73,3,14,7,0,73,17,1,0,0,0,10,21,
        29,37,40,48,52,57,60,62,66
    ]

class vba_likeParser ( Parser ):

    grammarFileName = "vba_like.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'-'", "']'", "'['", "'!'", "<INVALID>", 
                     "'?'", "'*'", "'#'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "CHAR", "WILD_CHAR", "WILD_SEQ", "WILD_DIGIT" ]

    RULE_program = 0
    RULE_likePatternElement = 1
    RULE_likePatternChar = 2
    RULE_wildcard = 3
    RULE_likePatternCharlist = 4
    RULE_charList = 5
    RULE_charListElement = 6
    RULE_charlistChar = 7
    RULE_charRange = 8

    ruleNames =  [ "program", "likePatternElement", "likePatternChar", "wildcard", 
                   "likePatternCharlist", "charList", "charListElement", 
                   "charlistChar", "charRange" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    CHAR=5
    WILD_CHAR=6
    WILD_SEQ=7
    WILD_DIGIT=8

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(vba_likeParser.EOF, 0)

        def likePatternElement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vba_likeParser.LikePatternElementContext)
            else:
                return self.getTypedRuleContext(vba_likeParser.LikePatternElementContext,i)


        def getRuleIndex(self):
            return vba_likeParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = vba_likeParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 21
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 494) != 0):
                self.state = 18
                self.likePatternElement()
                self.state = 23
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 24
            self.match(vba_likeParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LikePatternElementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def likePatternChar(self):
            return self.getTypedRuleContext(vba_likeParser.LikePatternCharContext,0)


        def likePatternCharlist(self):
            return self.getTypedRuleContext(vba_likeParser.LikePatternCharlistContext,0)


        def wildcard(self):
            return self.getTypedRuleContext(vba_likeParser.WildcardContext,0)


        def getRuleIndex(self):
            return vba_likeParser.RULE_likePatternElement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLikePatternElement" ):
                listener.enterLikePatternElement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLikePatternElement" ):
                listener.exitLikePatternElement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLikePatternElement" ):
                return visitor.visitLikePatternElement(self)
            else:
                return visitor.visitChildren(self)




    def likePatternElement(self):

        localctx = vba_likeParser.LikePatternElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_likePatternElement)
        try:
            self.state = 29
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2, 5]:
                self.enterOuterAlt(localctx, 1)
                self.state = 26
                self.likePatternChar()
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 27
                self.likePatternCharlist()
                pass
            elif token in [6, 7, 8]:
                self.enterOuterAlt(localctx, 3)
                self.state = 28
                self.wildcard()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LikePatternCharContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CHAR(self):
            return self.getToken(vba_likeParser.CHAR, 0)

        def getRuleIndex(self):
            return vba_likeParser.RULE_likePatternChar

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLikePatternChar" ):
                listener.enterLikePatternChar(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLikePatternChar" ):
                listener.exitLikePatternChar(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLikePatternChar" ):
                return visitor.visitLikePatternChar(self)
            else:
                return visitor.visitChildren(self)




    def likePatternChar(self):

        localctx = vba_likeParser.LikePatternCharContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_likePatternChar)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 31
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 38) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WildcardContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WILD_CHAR(self):
            return self.getToken(vba_likeParser.WILD_CHAR, 0)

        def WILD_SEQ(self):
            return self.getToken(vba_likeParser.WILD_SEQ, 0)

        def WILD_DIGIT(self):
            return self.getToken(vba_likeParser.WILD_DIGIT, 0)

        def getRuleIndex(self):
            return vba_likeParser.RULE_wildcard

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWildcard" ):
                listener.enterWildcard(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWildcard" ):
                listener.exitWildcard(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWildcard" ):
                return visitor.visitWildcard(self)
            else:
                return visitor.visitChildren(self)




    def wildcard(self):

        localctx = vba_likeParser.WildcardContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_wildcard)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 33
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 448) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LikePatternCharlistContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def charList(self):
            return self.getTypedRuleContext(vba_likeParser.CharListContext,0)


        def getRuleIndex(self):
            return vba_likeParser.RULE_likePatternCharlist

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLikePatternCharlist" ):
                listener.enterLikePatternCharlist(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLikePatternCharlist" ):
                listener.exitLikePatternCharlist(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLikePatternCharlist" ):
                return visitor.visitLikePatternCharlist(self)
            else:
                return visitor.visitChildren(self)




    def likePatternCharlist(self):

        localctx = vba_likeParser.LikePatternCharlistContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_likePatternCharlist)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            self.match(vba_likeParser.T__2)
            self.state = 37
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 36
                self.match(vba_likeParser.T__3)


            self.state = 40
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 490) != 0):
                self.state = 39
                self.charList()


            self.state = 42
            self.match(vba_likeParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CharListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def charListElement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vba_likeParser.CharListElementContext)
            else:
                return self.getTypedRuleContext(vba_likeParser.CharListElementContext,i)


        def getRuleIndex(self):
            return vba_likeParser.RULE_charList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCharList" ):
                listener.enterCharList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCharList" ):
                listener.exitCharList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCharList" ):
                return visitor.visitCharList(self)
            else:
                return visitor.visitChildren(self)




    def charList(self):

        localctx = vba_likeParser.CharListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_charList)
        self._la = 0 # Token type
        try:
            self.state = 62
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 44
                self.match(vba_likeParser.T__0)
                self.state = 48
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 488) != 0):
                    self.state = 45
                    self.charListElement()
                    self.state = 50
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 52
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==1:
                    self.state = 51
                    self.match(vba_likeParser.T__0)


                pass
            elif token in [3, 5, 6, 7, 8]:
                self.enterOuterAlt(localctx, 2)
                self.state = 55 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 54
                    self.charListElement()
                    self.state = 57 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 488) != 0)):
                        break

                self.state = 60
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==1:
                    self.state = 59
                    self.match(vba_likeParser.T__0)


                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CharListElementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def charlistChar(self):
            return self.getTypedRuleContext(vba_likeParser.CharlistCharContext,0)


        def charRange(self):
            return self.getTypedRuleContext(vba_likeParser.CharRangeContext,0)


        def getRuleIndex(self):
            return vba_likeParser.RULE_charListElement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCharListElement" ):
                listener.enterCharListElement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCharListElement" ):
                listener.exitCharListElement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCharListElement" ):
                return visitor.visitCharListElement(self)
            else:
                return visitor.visitChildren(self)




    def charListElement(self):

        localctx = vba_likeParser.CharListElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_charListElement)
        try:
            self.state = 66
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 64
                self.charlistChar()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 65
                self.charRange()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CharlistCharContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CHAR(self):
            return self.getToken(vba_likeParser.CHAR, 0)

        def WILD_SEQ(self):
            return self.getToken(vba_likeParser.WILD_SEQ, 0)

        def WILD_DIGIT(self):
            return self.getToken(vba_likeParser.WILD_DIGIT, 0)

        def WILD_CHAR(self):
            return self.getToken(vba_likeParser.WILD_CHAR, 0)

        def getRuleIndex(self):
            return vba_likeParser.RULE_charlistChar

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCharlistChar" ):
                listener.enterCharlistChar(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCharlistChar" ):
                listener.exitCharlistChar(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCharlistChar" ):
                return visitor.visitCharlistChar(self)
            else:
                return visitor.visitChildren(self)




    def charlistChar(self):

        localctx = vba_likeParser.CharlistCharContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_charlistChar)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 68
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 488) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CharRangeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def charlistChar(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vba_likeParser.CharlistCharContext)
            else:
                return self.getTypedRuleContext(vba_likeParser.CharlistCharContext,i)


        def getRuleIndex(self):
            return vba_likeParser.RULE_charRange

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCharRange" ):
                listener.enterCharRange(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCharRange" ):
                listener.exitCharRange(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCharRange" ):
                return visitor.visitCharRange(self)
            else:
                return visitor.visitChildren(self)




    def charRange(self):

        localctx = vba_likeParser.CharRangeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_charRange)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 70
            self.charlistChar()
            self.state = 71
            self.match(vba_likeParser.T__0)
            self.state = 72
            self.charlistChar()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx






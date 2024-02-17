# Generated from vba_like.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .vba_likeParser import vba_likeParser
else:
    from vba_likeParser import vba_likeParser

# This class defines a complete listener for a parse tree produced by vba_likeParser.
class vba_likeListener(ParseTreeListener):

    # Enter a parse tree produced by vba_likeParser#program.
    def enterProgram(self, ctx:vba_likeParser.ProgramContext):
        pass

    # Exit a parse tree produced by vba_likeParser#program.
    def exitProgram(self, ctx:vba_likeParser.ProgramContext):
        pass


    # Enter a parse tree produced by vba_likeParser#likePatternElement.
    def enterLikePatternElement(self, ctx:vba_likeParser.LikePatternElementContext):
        pass

    # Exit a parse tree produced by vba_likeParser#likePatternElement.
    def exitLikePatternElement(self, ctx:vba_likeParser.LikePatternElementContext):
        pass


    # Enter a parse tree produced by vba_likeParser#likePatternChar.
    def enterLikePatternChar(self, ctx:vba_likeParser.LikePatternCharContext):
        pass

    # Exit a parse tree produced by vba_likeParser#likePatternChar.
    def exitLikePatternChar(self, ctx:vba_likeParser.LikePatternCharContext):
        pass


    # Enter a parse tree produced by vba_likeParser#wildcard.
    def enterWildcard(self, ctx:vba_likeParser.WildcardContext):
        pass

    # Exit a parse tree produced by vba_likeParser#wildcard.
    def exitWildcard(self, ctx:vba_likeParser.WildcardContext):
        pass


    # Enter a parse tree produced by vba_likeParser#likePatternCharlist.
    def enterLikePatternCharlist(self, ctx:vba_likeParser.LikePatternCharlistContext):
        pass

    # Exit a parse tree produced by vba_likeParser#likePatternCharlist.
    def exitLikePatternCharlist(self, ctx:vba_likeParser.LikePatternCharlistContext):
        pass


    # Enter a parse tree produced by vba_likeParser#charList.
    def enterCharList(self, ctx:vba_likeParser.CharListContext):
        pass

    # Exit a parse tree produced by vba_likeParser#charList.
    def exitCharList(self, ctx:vba_likeParser.CharListContext):
        pass


    # Enter a parse tree produced by vba_likeParser#charListElement.
    def enterCharListElement(self, ctx:vba_likeParser.CharListElementContext):
        pass

    # Exit a parse tree produced by vba_likeParser#charListElement.
    def exitCharListElement(self, ctx:vba_likeParser.CharListElementContext):
        pass


    # Enter a parse tree produced by vba_likeParser#charlistChar.
    def enterCharlistChar(self, ctx:vba_likeParser.CharlistCharContext):
        pass

    # Exit a parse tree produced by vba_likeParser#charlistChar.
    def exitCharlistChar(self, ctx:vba_likeParser.CharlistCharContext):
        pass


    # Enter a parse tree produced by vba_likeParser#charRange.
    def enterCharRange(self, ctx:vba_likeParser.CharRangeContext):
        pass

    # Exit a parse tree produced by vba_likeParser#charRange.
    def exitCharRange(self, ctx:vba_likeParser.CharRangeContext):
        pass



del vba_likeParser
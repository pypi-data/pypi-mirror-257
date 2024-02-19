# Generated from vba_like.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .vba_likeParser import vba_likeParser
else:
    from vba_likeParser import vba_likeParser

# This class defines a complete generic visitor for a parse tree produced by vba_likeParser.

class vba_likeVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by vba_likeParser#program.
    def visitProgram(self, ctx:vba_likeParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_likeParser#likePatternElement.
    def visitLikePatternElement(self, ctx:vba_likeParser.LikePatternElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_likeParser#likePatternChar.
    def visitLikePatternChar(self, ctx:vba_likeParser.LikePatternCharContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_likeParser#wildcard.
    def visitWildcard(self, ctx:vba_likeParser.WildcardContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_likeParser#likePatternCharlist.
    def visitLikePatternCharlist(self, ctx:vba_likeParser.LikePatternCharlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_likeParser#charList.
    def visitCharList(self, ctx:vba_likeParser.CharListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_likeParser#charListElement.
    def visitCharListElement(self, ctx:vba_likeParser.CharListElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_likeParser#charlistChar.
    def visitCharlistChar(self, ctx:vba_likeParser.CharlistCharContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_likeParser#charRange.
    def visitCharRange(self, ctx:vba_likeParser.CharRangeContext):
        return self.visitChildren(ctx)



del vba_likeParser
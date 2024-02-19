# Generated from vba_cc.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .vba_ccParser import vba_ccParser
else:
    from vba_ccParser import vba_ccParser

# This class defines a complete generic visitor for a parse tree produced by vba_ccParser.

class vba_ccVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by vba_ccParser#startRule.
    def visitStartRule(self, ctx:vba_ccParser.StartRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#proceduralModuleHeader.
    def visitProceduralModuleHeader(self, ctx:vba_ccParser.ProceduralModuleHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#classFileHeader.
    def visitClassFileHeader(self, ctx:vba_ccParser.ClassFileHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#logicalLine.
    def visitLogicalLine(self, ctx:vba_ccParser.LogicalLineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#conditionalModuleBody.
    def visitConditionalModuleBody(self, ctx:vba_ccParser.ConditionalModuleBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#ccBlock.
    def visitCcBlock(self, ctx:vba_ccParser.CcBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#ccConst.
    def visitCcConst(self, ctx:vba_ccParser.CcConstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#ccVarLhs.
    def visitCcVarLhs(self, ctx:vba_ccParser.CcVarLhsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#ccIfBlock.
    def visitCcIfBlock(self, ctx:vba_ccParser.CcIfBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#ccIf.
    def visitCcIf(self, ctx:vba_ccParser.CcIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#ccElseifBlock.
    def visitCcElseifBlock(self, ctx:vba_ccParser.CcElseifBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#ccElseif.
    def visitCcElseif(self, ctx:vba_ccParser.CcElseifContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#ccElseBlock.
    def visitCcElseBlock(self, ctx:vba_ccParser.CcElseBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#ccElse.
    def visitCcElse(self, ctx:vba_ccParser.CcElseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#ccEndif.
    def visitCcEndif(self, ctx:vba_ccParser.CcEndifContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#ParenthesizedExpression.
    def visitParenthesizedExpression(self, ctx:vba_ccParser.ParenthesizedExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#LiteralExpress.
    def visitLiteralExpress(self, ctx:vba_ccParser.LiteralExpressContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#UnaryMinusExpression.
    def visitUnaryMinusExpression(self, ctx:vba_ccParser.UnaryMinusExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#RelationExpression.
    def visitRelationExpression(self, ctx:vba_ccParser.RelationExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#IndexExpression.
    def visitIndexExpression(self, ctx:vba_ccParser.IndexExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#NotOperatorExpression.
    def visitNotOperatorExpression(self, ctx:vba_ccParser.NotOperatorExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#ConcatExpression.
    def visitConcatExpression(self, ctx:vba_ccParser.ConcatExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#ArithmeticExpression.
    def visitArithmeticExpression(self, ctx:vba_ccParser.ArithmeticExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#booleanExpression.
    def visitBooleanExpression(self, ctx:vba_ccParser.BooleanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#IdentifierExpression.
    def visitIdentifierExpression(self, ctx:vba_ccParser.IdentifierExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#literalExpression.
    def visitLiteralExpression(self, ctx:vba_ccParser.LiteralExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#ccFunc.
    def visitCcFunc(self, ctx:vba_ccParser.CcFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vba_ccParser#reservedKeywords.
    def visitReservedKeywords(self, ctx:vba_ccParser.ReservedKeywordsContext):
        return self.visitChildren(ctx)



del vba_ccParser
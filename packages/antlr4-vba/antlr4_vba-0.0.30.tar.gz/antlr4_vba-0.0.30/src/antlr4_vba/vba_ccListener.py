# Generated from vba_cc.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .vba_ccParser import vba_ccParser
else:
    from vba_ccParser import vba_ccParser

# This class defines a complete listener for a parse tree produced by vba_ccParser.
class vba_ccListener(ParseTreeListener):

    # Enter a parse tree produced by vba_ccParser#startRule.
    def enterStartRule(self, ctx:vba_ccParser.StartRuleContext):
        pass

    # Exit a parse tree produced by vba_ccParser#startRule.
    def exitStartRule(self, ctx:vba_ccParser.StartRuleContext):
        pass


    # Enter a parse tree produced by vba_ccParser#proceduralModuleHeader.
    def enterProceduralModuleHeader(self, ctx:vba_ccParser.ProceduralModuleHeaderContext):
        pass

    # Exit a parse tree produced by vba_ccParser#proceduralModuleHeader.
    def exitProceduralModuleHeader(self, ctx:vba_ccParser.ProceduralModuleHeaderContext):
        pass


    # Enter a parse tree produced by vba_ccParser#classFileHeader.
    def enterClassFileHeader(self, ctx:vba_ccParser.ClassFileHeaderContext):
        pass

    # Exit a parse tree produced by vba_ccParser#classFileHeader.
    def exitClassFileHeader(self, ctx:vba_ccParser.ClassFileHeaderContext):
        pass


    # Enter a parse tree produced by vba_ccParser#logicalLine.
    def enterLogicalLine(self, ctx:vba_ccParser.LogicalLineContext):
        pass

    # Exit a parse tree produced by vba_ccParser#logicalLine.
    def exitLogicalLine(self, ctx:vba_ccParser.LogicalLineContext):
        pass


    # Enter a parse tree produced by vba_ccParser#conditionalModuleBody.
    def enterConditionalModuleBody(self, ctx:vba_ccParser.ConditionalModuleBodyContext):
        pass

    # Exit a parse tree produced by vba_ccParser#conditionalModuleBody.
    def exitConditionalModuleBody(self, ctx:vba_ccParser.ConditionalModuleBodyContext):
        pass


    # Enter a parse tree produced by vba_ccParser#ccBlock.
    def enterCcBlock(self, ctx:vba_ccParser.CcBlockContext):
        pass

    # Exit a parse tree produced by vba_ccParser#ccBlock.
    def exitCcBlock(self, ctx:vba_ccParser.CcBlockContext):
        pass


    # Enter a parse tree produced by vba_ccParser#ccConst.
    def enterCcConst(self, ctx:vba_ccParser.CcConstContext):
        pass

    # Exit a parse tree produced by vba_ccParser#ccConst.
    def exitCcConst(self, ctx:vba_ccParser.CcConstContext):
        pass


    # Enter a parse tree produced by vba_ccParser#ccVarLhs.
    def enterCcVarLhs(self, ctx:vba_ccParser.CcVarLhsContext):
        pass

    # Exit a parse tree produced by vba_ccParser#ccVarLhs.
    def exitCcVarLhs(self, ctx:vba_ccParser.CcVarLhsContext):
        pass


    # Enter a parse tree produced by vba_ccParser#ccIfBlock.
    def enterCcIfBlock(self, ctx:vba_ccParser.CcIfBlockContext):
        pass

    # Exit a parse tree produced by vba_ccParser#ccIfBlock.
    def exitCcIfBlock(self, ctx:vba_ccParser.CcIfBlockContext):
        pass


    # Enter a parse tree produced by vba_ccParser#ccIf.
    def enterCcIf(self, ctx:vba_ccParser.CcIfContext):
        pass

    # Exit a parse tree produced by vba_ccParser#ccIf.
    def exitCcIf(self, ctx:vba_ccParser.CcIfContext):
        pass


    # Enter a parse tree produced by vba_ccParser#ccElseifBlock.
    def enterCcElseifBlock(self, ctx:vba_ccParser.CcElseifBlockContext):
        pass

    # Exit a parse tree produced by vba_ccParser#ccElseifBlock.
    def exitCcElseifBlock(self, ctx:vba_ccParser.CcElseifBlockContext):
        pass


    # Enter a parse tree produced by vba_ccParser#ccElseif.
    def enterCcElseif(self, ctx:vba_ccParser.CcElseifContext):
        pass

    # Exit a parse tree produced by vba_ccParser#ccElseif.
    def exitCcElseif(self, ctx:vba_ccParser.CcElseifContext):
        pass


    # Enter a parse tree produced by vba_ccParser#ccElseBlock.
    def enterCcElseBlock(self, ctx:vba_ccParser.CcElseBlockContext):
        pass

    # Exit a parse tree produced by vba_ccParser#ccElseBlock.
    def exitCcElseBlock(self, ctx:vba_ccParser.CcElseBlockContext):
        pass


    # Enter a parse tree produced by vba_ccParser#ccElse.
    def enterCcElse(self, ctx:vba_ccParser.CcElseContext):
        pass

    # Exit a parse tree produced by vba_ccParser#ccElse.
    def exitCcElse(self, ctx:vba_ccParser.CcElseContext):
        pass


    # Enter a parse tree produced by vba_ccParser#ccEndif.
    def enterCcEndif(self, ctx:vba_ccParser.CcEndifContext):
        pass

    # Exit a parse tree produced by vba_ccParser#ccEndif.
    def exitCcEndif(self, ctx:vba_ccParser.CcEndifContext):
        pass


    # Enter a parse tree produced by vba_ccParser#ParenthesizedExpression.
    def enterParenthesizedExpression(self, ctx:vba_ccParser.ParenthesizedExpressionContext):
        pass

    # Exit a parse tree produced by vba_ccParser#ParenthesizedExpression.
    def exitParenthesizedExpression(self, ctx:vba_ccParser.ParenthesizedExpressionContext):
        pass


    # Enter a parse tree produced by vba_ccParser#LiteralExpress.
    def enterLiteralExpress(self, ctx:vba_ccParser.LiteralExpressContext):
        pass

    # Exit a parse tree produced by vba_ccParser#LiteralExpress.
    def exitLiteralExpress(self, ctx:vba_ccParser.LiteralExpressContext):
        pass


    # Enter a parse tree produced by vba_ccParser#UnaryMinusExpression.
    def enterUnaryMinusExpression(self, ctx:vba_ccParser.UnaryMinusExpressionContext):
        pass

    # Exit a parse tree produced by vba_ccParser#UnaryMinusExpression.
    def exitUnaryMinusExpression(self, ctx:vba_ccParser.UnaryMinusExpressionContext):
        pass


    # Enter a parse tree produced by vba_ccParser#RelationExpression.
    def enterRelationExpression(self, ctx:vba_ccParser.RelationExpressionContext):
        pass

    # Exit a parse tree produced by vba_ccParser#RelationExpression.
    def exitRelationExpression(self, ctx:vba_ccParser.RelationExpressionContext):
        pass


    # Enter a parse tree produced by vba_ccParser#IndexExpression.
    def enterIndexExpression(self, ctx:vba_ccParser.IndexExpressionContext):
        pass

    # Exit a parse tree produced by vba_ccParser#IndexExpression.
    def exitIndexExpression(self, ctx:vba_ccParser.IndexExpressionContext):
        pass


    # Enter a parse tree produced by vba_ccParser#NotOperatorExpression.
    def enterNotOperatorExpression(self, ctx:vba_ccParser.NotOperatorExpressionContext):
        pass

    # Exit a parse tree produced by vba_ccParser#NotOperatorExpression.
    def exitNotOperatorExpression(self, ctx:vba_ccParser.NotOperatorExpressionContext):
        pass


    # Enter a parse tree produced by vba_ccParser#ConcatExpression.
    def enterConcatExpression(self, ctx:vba_ccParser.ConcatExpressionContext):
        pass

    # Exit a parse tree produced by vba_ccParser#ConcatExpression.
    def exitConcatExpression(self, ctx:vba_ccParser.ConcatExpressionContext):
        pass


    # Enter a parse tree produced by vba_ccParser#ArithmeticExpression.
    def enterArithmeticExpression(self, ctx:vba_ccParser.ArithmeticExpressionContext):
        pass

    # Exit a parse tree produced by vba_ccParser#ArithmeticExpression.
    def exitArithmeticExpression(self, ctx:vba_ccParser.ArithmeticExpressionContext):
        pass


    # Enter a parse tree produced by vba_ccParser#booleanExpression.
    def enterBooleanExpression(self, ctx:vba_ccParser.BooleanExpressionContext):
        pass

    # Exit a parse tree produced by vba_ccParser#booleanExpression.
    def exitBooleanExpression(self, ctx:vba_ccParser.BooleanExpressionContext):
        pass


    # Enter a parse tree produced by vba_ccParser#IdentifierExpression.
    def enterIdentifierExpression(self, ctx:vba_ccParser.IdentifierExpressionContext):
        pass

    # Exit a parse tree produced by vba_ccParser#IdentifierExpression.
    def exitIdentifierExpression(self, ctx:vba_ccParser.IdentifierExpressionContext):
        pass


    # Enter a parse tree produced by vba_ccParser#literalExpression.
    def enterLiteralExpression(self, ctx:vba_ccParser.LiteralExpressionContext):
        pass

    # Exit a parse tree produced by vba_ccParser#literalExpression.
    def exitLiteralExpression(self, ctx:vba_ccParser.LiteralExpressionContext):
        pass


    # Enter a parse tree produced by vba_ccParser#ccFunc.
    def enterCcFunc(self, ctx:vba_ccParser.CcFuncContext):
        pass

    # Exit a parse tree produced by vba_ccParser#ccFunc.
    def exitCcFunc(self, ctx:vba_ccParser.CcFuncContext):
        pass


    # Enter a parse tree produced by vba_ccParser#reservedKeywords.
    def enterReservedKeywords(self, ctx:vba_ccParser.ReservedKeywordsContext):
        pass

    # Exit a parse tree produced by vba_ccParser#reservedKeywords.
    def exitReservedKeywords(self, ctx:vba_ccParser.ReservedKeywordsContext):
        pass



del vba_ccParser
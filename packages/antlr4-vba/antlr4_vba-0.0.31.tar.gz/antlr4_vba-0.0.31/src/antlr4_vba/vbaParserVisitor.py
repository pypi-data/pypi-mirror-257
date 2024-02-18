# Generated from vbaParser.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .vbaParser import vbaParser
else:
    from vbaParser import vbaParser

# This class defines a complete generic visitor for a parse tree produced by vbaParser.

class vbaParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by vbaParser#startRule.
    def visitStartRule(self, ctx:vbaParser.StartRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#module.
    def visitModule(self, ctx:vbaParser.ModuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#classFileHeader.
    def visitClassFileHeader(self, ctx:vbaParser.ClassFileHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#classVersionIdentification.
    def visitClassVersionIdentification(self, ctx:vbaParser.ClassVersionIdentificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#classBeginBlock.
    def visitClassBeginBlock(self, ctx:vbaParser.ClassBeginBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#beginBlockConfigElement.
    def visitBeginBlockConfigElement(self, ctx:vbaParser.BeginBlockConfigElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#proceduralModule.
    def visitProceduralModule(self, ctx:vbaParser.ProceduralModuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#classModule.
    def visitClassModule(self, ctx:vbaParser.ClassModuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#proceduralModuleHeader.
    def visitProceduralModuleHeader(self, ctx:vbaParser.ProceduralModuleHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#classModuleHeader.
    def visitClassModuleHeader(self, ctx:vbaParser.ClassModuleHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#classAttr.
    def visitClassAttr(self, ctx:vbaParser.ClassAttrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#proceduralModuleBody.
    def visitProceduralModuleBody(self, ctx:vbaParser.ProceduralModuleBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#classModuleBody.
    def visitClassModuleBody(self, ctx:vbaParser.ClassModuleBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#unrestrictedName.
    def visitUnrestrictedName(self, ctx:vbaParser.UnrestrictedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#name.
    def visitName(self, ctx:vbaParser.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#untypedName.
    def visitUntypedName(self, ctx:vbaParser.UntypedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#proceduralModuleDeclarationSection.
    def visitProceduralModuleDeclarationSection(self, ctx:vbaParser.ProceduralModuleDeclarationSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#classModuleDeclarationSection.
    def visitClassModuleDeclarationSection(self, ctx:vbaParser.ClassModuleDeclarationSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#proceduralModuleDirectiveElement.
    def visitProceduralModuleDirectiveElement(self, ctx:vbaParser.ProceduralModuleDirectiveElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#proceduralModuleDeclarationElement.
    def visitProceduralModuleDeclarationElement(self, ctx:vbaParser.ProceduralModuleDeclarationElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#classModuleDirectiveElement.
    def visitClassModuleDirectiveElement(self, ctx:vbaParser.ClassModuleDirectiveElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#classModuleDeclarationElement.
    def visitClassModuleDeclarationElement(self, ctx:vbaParser.ClassModuleDeclarationElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#commonOptionDirective.
    def visitCommonOptionDirective(self, ctx:vbaParser.CommonOptionDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#optionCompareDirective.
    def visitOptionCompareDirective(self, ctx:vbaParser.OptionCompareDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#optionBaseDirective.
    def visitOptionBaseDirective(self, ctx:vbaParser.OptionBaseDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#optionExplicitDirective.
    def visitOptionExplicitDirective(self, ctx:vbaParser.OptionExplicitDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#optionPrivateDirective.
    def visitOptionPrivateDirective(self, ctx:vbaParser.OptionPrivateDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#defDirective.
    def visitDefDirective(self, ctx:vbaParser.DefDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#letterSpec.
    def visitLetterSpec(self, ctx:vbaParser.LetterSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#singleLetter.
    def visitSingleLetter(self, ctx:vbaParser.SingleLetterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#universalLetterRange.
    def visitUniversalLetterRange(self, ctx:vbaParser.UniversalLetterRangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#upperCaseA.
    def visitUpperCaseA(self, ctx:vbaParser.UpperCaseAContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#upperCaseZ.
    def visitUpperCaseZ(self, ctx:vbaParser.UpperCaseZContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#letterRange.
    def visitLetterRange(self, ctx:vbaParser.LetterRangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#firstLetter.
    def visitFirstLetter(self, ctx:vbaParser.FirstLetterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#lastLetter.
    def visitLastLetter(self, ctx:vbaParser.LastLetterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#defType.
    def visitDefType(self, ctx:vbaParser.DefTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#commonModuleDeclarationElement.
    def visitCommonModuleDeclarationElement(self, ctx:vbaParser.CommonModuleDeclarationElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#moduleVariableDeclaration.
    def visitModuleVariableDeclaration(self, ctx:vbaParser.ModuleVariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#globalVariableDeclaration.
    def visitGlobalVariableDeclaration(self, ctx:vbaParser.GlobalVariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#publicVariableDecalation.
    def visitPublicVariableDecalation(self, ctx:vbaParser.PublicVariableDecalationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#privateVariableDeclaration.
    def visitPrivateVariableDeclaration(self, ctx:vbaParser.PrivateVariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#moduleVariableDeclarationList.
    def visitModuleVariableDeclarationList(self, ctx:vbaParser.ModuleVariableDeclarationListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#variableDeclarationList.
    def visitVariableDeclarationList(self, ctx:vbaParser.VariableDeclarationListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#variableDcl.
    def visitVariableDcl(self, ctx:vbaParser.VariableDclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#typedVariableDcl.
    def visitTypedVariableDcl(self, ctx:vbaParser.TypedVariableDclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#untypedVariableDcl.
    def visitUntypedVariableDcl(self, ctx:vbaParser.UntypedVariableDclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#arrayClause.
    def visitArrayClause(self, ctx:vbaParser.ArrayClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#asClause.
    def visitAsClause(self, ctx:vbaParser.AsClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#witheventsVariableDcl.
    def visitWitheventsVariableDcl(self, ctx:vbaParser.WitheventsVariableDclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#classTypeName.
    def visitClassTypeName(self, ctx:vbaParser.ClassTypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#arrayDim.
    def visitArrayDim(self, ctx:vbaParser.ArrayDimContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#boundsList.
    def visitBoundsList(self, ctx:vbaParser.BoundsListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#dimSpec.
    def visitDimSpec(self, ctx:vbaParser.DimSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#lowerBound.
    def visitLowerBound(self, ctx:vbaParser.LowerBoundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#upperBound.
    def visitUpperBound(self, ctx:vbaParser.UpperBoundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#asAutoObject.
    def visitAsAutoObject(self, ctx:vbaParser.AsAutoObjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#asType.
    def visitAsType(self, ctx:vbaParser.AsTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#typeSpec.
    def visitTypeSpec(self, ctx:vbaParser.TypeSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#fixedLengthStringSpec.
    def visitFixedLengthStringSpec(self, ctx:vbaParser.FixedLengthStringSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#stringLength.
    def visitStringLength(self, ctx:vbaParser.StringLengthContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#constantName.
    def visitConstantName(self, ctx:vbaParser.ConstantNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#publicConstDeclaration.
    def visitPublicConstDeclaration(self, ctx:vbaParser.PublicConstDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#privateConstDeclaration.
    def visitPrivateConstDeclaration(self, ctx:vbaParser.PrivateConstDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#moduleConstDeclaration.
    def visitModuleConstDeclaration(self, ctx:vbaParser.ModuleConstDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#constDeclaration.
    def visitConstDeclaration(self, ctx:vbaParser.ConstDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#constItemList.
    def visitConstItemList(self, ctx:vbaParser.ConstItemListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#constItem.
    def visitConstItem(self, ctx:vbaParser.ConstItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#typedNameConstItem.
    def visitTypedNameConstItem(self, ctx:vbaParser.TypedNameConstItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#untypedNameConstItem.
    def visitUntypedNameConstItem(self, ctx:vbaParser.UntypedNameConstItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#constAsClause.
    def visitConstAsClause(self, ctx:vbaParser.ConstAsClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#publicTypeDeclaration.
    def visitPublicTypeDeclaration(self, ctx:vbaParser.PublicTypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#privateTypeDeclaration.
    def visitPrivateTypeDeclaration(self, ctx:vbaParser.PrivateTypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#udtDeclaration.
    def visitUdtDeclaration(self, ctx:vbaParser.UdtDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#udtMemberList.
    def visitUdtMemberList(self, ctx:vbaParser.UdtMemberListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#udtElement.
    def visitUdtElement(self, ctx:vbaParser.UdtElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#udtMember.
    def visitUdtMember(self, ctx:vbaParser.UdtMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#untypedNameMemberDcl.
    def visitUntypedNameMemberDcl(self, ctx:vbaParser.UntypedNameMemberDclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#reservedNameMemberDcl.
    def visitReservedNameMemberDcl(self, ctx:vbaParser.ReservedNameMemberDclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#optionalArrayClause.
    def visitOptionalArrayClause(self, ctx:vbaParser.OptionalArrayClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#reservedMemberName.
    def visitReservedMemberName(self, ctx:vbaParser.ReservedMemberNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#globalEnumDeclaration.
    def visitGlobalEnumDeclaration(self, ctx:vbaParser.GlobalEnumDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#publicEnumDeclaration.
    def visitPublicEnumDeclaration(self, ctx:vbaParser.PublicEnumDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#privateEnumDeclaration.
    def visitPrivateEnumDeclaration(self, ctx:vbaParser.PrivateEnumDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#enumDeclaration.
    def visitEnumDeclaration(self, ctx:vbaParser.EnumDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#enumMemberList.
    def visitEnumMemberList(self, ctx:vbaParser.EnumMemberListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#enumElement.
    def visitEnumElement(self, ctx:vbaParser.EnumElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#enumMember.
    def visitEnumMember(self, ctx:vbaParser.EnumMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#publicExternalProcedureDeclaration.
    def visitPublicExternalProcedureDeclaration(self, ctx:vbaParser.PublicExternalProcedureDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#privateExternalProcedureDeclaration.
    def visitPrivateExternalProcedureDeclaration(self, ctx:vbaParser.PrivateExternalProcedureDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#externalProcDcl.
    def visitExternalProcDcl(self, ctx:vbaParser.ExternalProcDclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#externalSub.
    def visitExternalSub(self, ctx:vbaParser.ExternalSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#externalFunction.
    def visitExternalFunction(self, ctx:vbaParser.ExternalFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#libInfo.
    def visitLibInfo(self, ctx:vbaParser.LibInfoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#libClause.
    def visitLibClause(self, ctx:vbaParser.LibClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#aliasClause.
    def visitAliasClause(self, ctx:vbaParser.AliasClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#implementsDirective.
    def visitImplementsDirective(self, ctx:vbaParser.ImplementsDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#eventDeclaration.
    def visitEventDeclaration(self, ctx:vbaParser.EventDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#eventParameterList.
    def visitEventParameterList(self, ctx:vbaParser.EventParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#proceduralModuleCode.
    def visitProceduralModuleCode(self, ctx:vbaParser.ProceduralModuleCodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#classModuleCode.
    def visitClassModuleCode(self, ctx:vbaParser.ClassModuleCodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#proceduralModuleCodeElement.
    def visitProceduralModuleCodeElement(self, ctx:vbaParser.ProceduralModuleCodeElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#classModuleCodeElement.
    def visitClassModuleCodeElement(self, ctx:vbaParser.ClassModuleCodeElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#commonModuleCodeElement.
    def visitCommonModuleCodeElement(self, ctx:vbaParser.CommonModuleCodeElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#procedureDeclaration.
    def visitProcedureDeclaration(self, ctx:vbaParser.ProcedureDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#subroutineDeclaration.
    def visitSubroutineDeclaration(self, ctx:vbaParser.SubroutineDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#functionDeclaration.
    def visitFunctionDeclaration(self, ctx:vbaParser.FunctionDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#propertyGetDeclaration.
    def visitPropertyGetDeclaration(self, ctx:vbaParser.PropertyGetDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#propertyLhsDeclaration.
    def visitPropertyLhsDeclaration(self, ctx:vbaParser.PropertyLhsDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#endLabel.
    def visitEndLabel(self, ctx:vbaParser.EndLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#procedureTail.
    def visitProcedureTail(self, ctx:vbaParser.ProcedureTailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#procedureScope.
    def visitProcedureScope(self, ctx:vbaParser.ProcedureScopeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#initialStatic.
    def visitInitialStatic(self, ctx:vbaParser.InitialStaticContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#trailingStatic.
    def visitTrailingStatic(self, ctx:vbaParser.TrailingStaticContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#subroutineName.
    def visitSubroutineName(self, ctx:vbaParser.SubroutineNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#functionName.
    def visitFunctionName(self, ctx:vbaParser.FunctionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#prefixedName.
    def visitPrefixedName(self, ctx:vbaParser.PrefixedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#functionType.
    def visitFunctionType(self, ctx:vbaParser.FunctionTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#arrayDesignator.
    def visitArrayDesignator(self, ctx:vbaParser.ArrayDesignatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#procedureParameters.
    def visitProcedureParameters(self, ctx:vbaParser.ProcedureParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#propertyParameters.
    def visitPropertyParameters(self, ctx:vbaParser.PropertyParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#parameterList.
    def visitParameterList(self, ctx:vbaParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#positionalParameters.
    def visitPositionalParameters(self, ctx:vbaParser.PositionalParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#optionalParameters.
    def visitOptionalParameters(self, ctx:vbaParser.OptionalParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#valueParam.
    def visitValueParam(self, ctx:vbaParser.ValueParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#positionalParam.
    def visitPositionalParam(self, ctx:vbaParser.PositionalParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#optionalParam.
    def visitOptionalParam(self, ctx:vbaParser.OptionalParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#paramArray.
    def visitParamArray(self, ctx:vbaParser.ParamArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#paramDcl.
    def visitParamDcl(self, ctx:vbaParser.ParamDclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#untypedNameParamDcl.
    def visitUntypedNameParamDcl(self, ctx:vbaParser.UntypedNameParamDclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#typedNameParamDcl.
    def visitTypedNameParamDcl(self, ctx:vbaParser.TypedNameParamDclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#optionalPrefix.
    def visitOptionalPrefix(self, ctx:vbaParser.OptionalPrefixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#parameterMechanism.
    def visitParameterMechanism(self, ctx:vbaParser.ParameterMechanismContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#parameterType.
    def visitParameterType(self, ctx:vbaParser.ParameterTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#defaultValue.
    def visitDefaultValue(self, ctx:vbaParser.DefaultValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#eventHandlerName.
    def visitEventHandlerName(self, ctx:vbaParser.EventHandlerNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#implementedName.
    def visitImplementedName(self, ctx:vbaParser.ImplementedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#lifecycleHandlerName.
    def visitLifecycleHandlerName(self, ctx:vbaParser.LifecycleHandlerNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#procedureBody.
    def visitProcedureBody(self, ctx:vbaParser.ProcedureBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#statementBlock.
    def visitStatementBlock(self, ctx:vbaParser.StatementBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#blockStatement.
    def visitBlockStatement(self, ctx:vbaParser.BlockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#statement.
    def visitStatement(self, ctx:vbaParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#statementLabelDefinition.
    def visitStatementLabelDefinition(self, ctx:vbaParser.StatementLabelDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#statementLabel.
    def visitStatementLabel(self, ctx:vbaParser.StatementLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#statementLabelList.
    def visitStatementLabelList(self, ctx:vbaParser.StatementLabelListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#identifierStatementLabel.
    def visitIdentifierStatementLabel(self, ctx:vbaParser.IdentifierStatementLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#lineNumberLabel.
    def visitLineNumberLabel(self, ctx:vbaParser.LineNumberLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#remStatement.
    def visitRemStatement(self, ctx:vbaParser.RemStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#controlStatement.
    def visitControlStatement(self, ctx:vbaParser.ControlStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#controlStatementExceptMultilineIf.
    def visitControlStatementExceptMultilineIf(self, ctx:vbaParser.ControlStatementExceptMultilineIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#callStatement.
    def visitCallStatement(self, ctx:vbaParser.CallStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#whileStatement.
    def visitWhileStatement(self, ctx:vbaParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#forStatement.
    def visitForStatement(self, ctx:vbaParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#simpleForStatement.
    def visitSimpleForStatement(self, ctx:vbaParser.SimpleForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#explicitForStatement.
    def visitExplicitForStatement(self, ctx:vbaParser.ExplicitForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#nestedForStatement.
    def visitNestedForStatement(self, ctx:vbaParser.NestedForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#forClause.
    def visitForClause(self, ctx:vbaParser.ForClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#startValue.
    def visitStartValue(self, ctx:vbaParser.StartValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#endValue.
    def visitEndValue(self, ctx:vbaParser.EndValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#stepClause.
    def visitStepClause(self, ctx:vbaParser.StepClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#stepIncrement.
    def visitStepIncrement(self, ctx:vbaParser.StepIncrementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#forEachStatement.
    def visitForEachStatement(self, ctx:vbaParser.ForEachStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#simpleForEachStatement.
    def visitSimpleForEachStatement(self, ctx:vbaParser.SimpleForEachStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#explicitForEachStatement.
    def visitExplicitForEachStatement(self, ctx:vbaParser.ExplicitForEachStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#forEachClause.
    def visitForEachClause(self, ctx:vbaParser.ForEachClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#collection.
    def visitCollection(self, ctx:vbaParser.CollectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#exitForStatement.
    def visitExitForStatement(self, ctx:vbaParser.ExitForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#doStatement.
    def visitDoStatement(self, ctx:vbaParser.DoStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#conditionClause.
    def visitConditionClause(self, ctx:vbaParser.ConditionClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#whileClause.
    def visitWhileClause(self, ctx:vbaParser.WhileClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#untilClause.
    def visitUntilClause(self, ctx:vbaParser.UntilClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#exitDoStatement.
    def visitExitDoStatement(self, ctx:vbaParser.ExitDoStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#ifStatement.
    def visitIfStatement(self, ctx:vbaParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#elseIfBlock.
    def visitElseIfBlock(self, ctx:vbaParser.ElseIfBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#elseBlock.
    def visitElseBlock(self, ctx:vbaParser.ElseBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#singleLineIfStatement.
    def visitSingleLineIfStatement(self, ctx:vbaParser.SingleLineIfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#ifWithNonEmptyThen.
    def visitIfWithNonEmptyThen(self, ctx:vbaParser.IfWithNonEmptyThenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#ifWithEmptyThen.
    def visitIfWithEmptyThen(self, ctx:vbaParser.IfWithEmptyThenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#singleLineElseClause.
    def visitSingleLineElseClause(self, ctx:vbaParser.SingleLineElseClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#listOrLabel.
    def visitListOrLabel(self, ctx:vbaParser.ListOrLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#sameLineStatement.
    def visitSameLineStatement(self, ctx:vbaParser.SameLineStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#selectCaseStatement.
    def visitSelectCaseStatement(self, ctx:vbaParser.SelectCaseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#caseClause.
    def visitCaseClause(self, ctx:vbaParser.CaseClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#caseElseClause.
    def visitCaseElseClause(self, ctx:vbaParser.CaseElseClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#rangeClause.
    def visitRangeClause(self, ctx:vbaParser.RangeClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#selectExpression.
    def visitSelectExpression(self, ctx:vbaParser.SelectExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#comparisonOperator.
    def visitComparisonOperator(self, ctx:vbaParser.ComparisonOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#stopStatement.
    def visitStopStatement(self, ctx:vbaParser.StopStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#gotoStatement.
    def visitGotoStatement(self, ctx:vbaParser.GotoStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#onGotoStatement.
    def visitOnGotoStatement(self, ctx:vbaParser.OnGotoStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#gosubStatement.
    def visitGosubStatement(self, ctx:vbaParser.GosubStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#returnStatement.
    def visitReturnStatement(self, ctx:vbaParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#onGosubStatement.
    def visitOnGosubStatement(self, ctx:vbaParser.OnGosubStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#exitSubStatement.
    def visitExitSubStatement(self, ctx:vbaParser.ExitSubStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#exitFunctionStatement.
    def visitExitFunctionStatement(self, ctx:vbaParser.ExitFunctionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#exitPropertyStatement.
    def visitExitPropertyStatement(self, ctx:vbaParser.ExitPropertyStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#raiseeventStatement.
    def visitRaiseeventStatement(self, ctx:vbaParser.RaiseeventStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#eventArgumentList.
    def visitEventArgumentList(self, ctx:vbaParser.EventArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#eventArgument.
    def visitEventArgument(self, ctx:vbaParser.EventArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#withStatement.
    def visitWithStatement(self, ctx:vbaParser.WithStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#dataManipulationStatement.
    def visitDataManipulationStatement(self, ctx:vbaParser.DataManipulationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#localVariableDeclaration.
    def visitLocalVariableDeclaration(self, ctx:vbaParser.LocalVariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#staticVariableDeclaration.
    def visitStaticVariableDeclaration(self, ctx:vbaParser.StaticVariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#localConstDeclaration.
    def visitLocalConstDeclaration(self, ctx:vbaParser.LocalConstDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#redimStatement.
    def visitRedimStatement(self, ctx:vbaParser.RedimStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#redimDeclarationList.
    def visitRedimDeclarationList(self, ctx:vbaParser.RedimDeclarationListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#redimVariableDcl.
    def visitRedimVariableDcl(self, ctx:vbaParser.RedimVariableDclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#redimTypedVariableDcl.
    def visitRedimTypedVariableDcl(self, ctx:vbaParser.RedimTypedVariableDclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#redimUntypedDcl.
    def visitRedimUntypedDcl(self, ctx:vbaParser.RedimUntypedDclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#dynamicArrayDim.
    def visitDynamicArrayDim(self, ctx:vbaParser.DynamicArrayDimContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#dynamicBoundsList.
    def visitDynamicBoundsList(self, ctx:vbaParser.DynamicBoundsListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#dynamicDimSpec.
    def visitDynamicDimSpec(self, ctx:vbaParser.DynamicDimSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#dynamicLowerBound.
    def visitDynamicLowerBound(self, ctx:vbaParser.DynamicLowerBoundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#dynamicUpperBound.
    def visitDynamicUpperBound(self, ctx:vbaParser.DynamicUpperBoundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#dynamicArrayClause.
    def visitDynamicArrayClause(self, ctx:vbaParser.DynamicArrayClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#eraseStatement.
    def visitEraseStatement(self, ctx:vbaParser.EraseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#eraseList.
    def visitEraseList(self, ctx:vbaParser.EraseListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#eraseElement.
    def visitEraseElement(self, ctx:vbaParser.EraseElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#midStatement.
    def visitMidStatement(self, ctx:vbaParser.MidStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#modeSpecifier.
    def visitModeSpecifier(self, ctx:vbaParser.ModeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#stringArgument.
    def visitStringArgument(self, ctx:vbaParser.StringArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#startMid.
    def visitStartMid(self, ctx:vbaParser.StartMidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#length.
    def visitLength(self, ctx:vbaParser.LengthContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#lsetStatement.
    def visitLsetStatement(self, ctx:vbaParser.LsetStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#rsetStatement.
    def visitRsetStatement(self, ctx:vbaParser.RsetStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#letStatement.
    def visitLetStatement(self, ctx:vbaParser.LetStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#setStatement.
    def visitSetStatement(self, ctx:vbaParser.SetStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#errorHandlingStatement.
    def visitErrorHandlingStatement(self, ctx:vbaParser.ErrorHandlingStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#onErrorStatement.
    def visitOnErrorStatement(self, ctx:vbaParser.OnErrorStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#errorBehavior.
    def visitErrorBehavior(self, ctx:vbaParser.ErrorBehaviorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#resumeStatement.
    def visitResumeStatement(self, ctx:vbaParser.ResumeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#errorStatement.
    def visitErrorStatement(self, ctx:vbaParser.ErrorStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#errorNumber.
    def visitErrorNumber(self, ctx:vbaParser.ErrorNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#fileStatement.
    def visitFileStatement(self, ctx:vbaParser.FileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#openStatement.
    def visitOpenStatement(self, ctx:vbaParser.OpenStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#pathName.
    def visitPathName(self, ctx:vbaParser.PathNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#modeClause.
    def visitModeClause(self, ctx:vbaParser.ModeClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#modeOpt.
    def visitModeOpt(self, ctx:vbaParser.ModeOptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#accessClause.
    def visitAccessClause(self, ctx:vbaParser.AccessClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#access.
    def visitAccess(self, ctx:vbaParser.AccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#lock.
    def visitLock(self, ctx:vbaParser.LockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#lenClause.
    def visitLenClause(self, ctx:vbaParser.LenClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#recLength.
    def visitRecLength(self, ctx:vbaParser.RecLengthContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#fileNumber.
    def visitFileNumber(self, ctx:vbaParser.FileNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#markedFileNumber.
    def visitMarkedFileNumber(self, ctx:vbaParser.MarkedFileNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#unmarkedFileNumber.
    def visitUnmarkedFileNumber(self, ctx:vbaParser.UnmarkedFileNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#closeStatement.
    def visitCloseStatement(self, ctx:vbaParser.CloseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#fileNumberList.
    def visitFileNumberList(self, ctx:vbaParser.FileNumberListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#seekStatement.
    def visitSeekStatement(self, ctx:vbaParser.SeekStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#position.
    def visitPosition(self, ctx:vbaParser.PositionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#lockStatement.
    def visitLockStatement(self, ctx:vbaParser.LockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#recordRange.
    def visitRecordRange(self, ctx:vbaParser.RecordRangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#startRecordNumber.
    def visitStartRecordNumber(self, ctx:vbaParser.StartRecordNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#endRecordNumber.
    def visitEndRecordNumber(self, ctx:vbaParser.EndRecordNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#unlockStatement.
    def visitUnlockStatement(self, ctx:vbaParser.UnlockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#lineInputStatement.
    def visitLineInputStatement(self, ctx:vbaParser.LineInputStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#variableName.
    def visitVariableName(self, ctx:vbaParser.VariableNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#widthStatement.
    def visitWidthStatement(self, ctx:vbaParser.WidthStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#lineWidth.
    def visitLineWidth(self, ctx:vbaParser.LineWidthContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#printStatement.
    def visitPrintStatement(self, ctx:vbaParser.PrintStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#outputList.
    def visitOutputList(self, ctx:vbaParser.OutputListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#outputItem.
    def visitOutputItem(self, ctx:vbaParser.OutputItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#outputClause.
    def visitOutputClause(self, ctx:vbaParser.OutputClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#charPosition.
    def visitCharPosition(self, ctx:vbaParser.CharPositionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#outputExpression.
    def visitOutputExpression(self, ctx:vbaParser.OutputExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#spcClause.
    def visitSpcClause(self, ctx:vbaParser.SpcClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#spcNumber.
    def visitSpcNumber(self, ctx:vbaParser.SpcNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#tabClause.
    def visitTabClause(self, ctx:vbaParser.TabClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#tabNumber.
    def visitTabNumber(self, ctx:vbaParser.TabNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#writeStatement.
    def visitWriteStatement(self, ctx:vbaParser.WriteStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#inputStatement.
    def visitInputStatement(self, ctx:vbaParser.InputStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#inputList.
    def visitInputList(self, ctx:vbaParser.InputListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#inputVariable.
    def visitInputVariable(self, ctx:vbaParser.InputVariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#putStatement.
    def visitPutStatement(self, ctx:vbaParser.PutStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#recordNumber.
    def visitRecordNumber(self, ctx:vbaParser.RecordNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#data.
    def visitData(self, ctx:vbaParser.DataContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#getStatement.
    def visitGetStatement(self, ctx:vbaParser.GetStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#variable.
    def visitVariable(self, ctx:vbaParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#expression.
    def visitExpression(self, ctx:vbaParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#lExpression.
    def visitLExpression(self, ctx:vbaParser.LExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#literalExpression.
    def visitLiteralExpression(self, ctx:vbaParser.LiteralExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#parenthesizedExpression.
    def visitParenthesizedExpression(self, ctx:vbaParser.ParenthesizedExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#typeofIsExpression.
    def visitTypeofIsExpression(self, ctx:vbaParser.TypeofIsExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#newExpress.
    def visitNewExpress(self, ctx:vbaParser.NewExpressContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#notOperatorExpression.
    def visitNotOperatorExpression(self, ctx:vbaParser.NotOperatorExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#unaryMinusExpression.
    def visitUnaryMinusExpression(self, ctx:vbaParser.UnaryMinusExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#simpleNameExpression.
    def visitSimpleNameExpression(self, ctx:vbaParser.SimpleNameExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#instanceExpression.
    def visitInstanceExpression(self, ctx:vbaParser.InstanceExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#memberAccessExpression.
    def visitMemberAccessExpression(self, ctx:vbaParser.MemberAccessExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#indexExpression.
    def visitIndexExpression(self, ctx:vbaParser.IndexExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#argumentList.
    def visitArgumentList(self, ctx:vbaParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#positionalOrNamedArgumentList.
    def visitPositionalOrNamedArgumentList(self, ctx:vbaParser.PositionalOrNamedArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#positionalArgument.
    def visitPositionalArgument(self, ctx:vbaParser.PositionalArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#requiredPositionalArgument.
    def visitRequiredPositionalArgument(self, ctx:vbaParser.RequiredPositionalArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#namedArgumentList.
    def visitNamedArgumentList(self, ctx:vbaParser.NamedArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#namedArgument.
    def visitNamedArgument(self, ctx:vbaParser.NamedArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#argumentExpression.
    def visitArgumentExpression(self, ctx:vbaParser.ArgumentExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#dictionaryAccessExpression.
    def visitDictionaryAccessExpression(self, ctx:vbaParser.DictionaryAccessExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#withExpression.
    def visitWithExpression(self, ctx:vbaParser.WithExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#withMemberAccessExpression.
    def visitWithMemberAccessExpression(self, ctx:vbaParser.WithMemberAccessExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#withDictionaryAccessExpression.
    def visitWithDictionaryAccessExpression(self, ctx:vbaParser.WithDictionaryAccessExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#constantExpression.
    def visitConstantExpression(self, ctx:vbaParser.ConstantExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#ccExpression.
    def visitCcExpression(self, ctx:vbaParser.CcExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#booleanExpression.
    def visitBooleanExpression(self, ctx:vbaParser.BooleanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#integerExpression.
    def visitIntegerExpression(self, ctx:vbaParser.IntegerExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#variableExpression.
    def visitVariableExpression(self, ctx:vbaParser.VariableExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#boundVariableExpression.
    def visitBoundVariableExpression(self, ctx:vbaParser.BoundVariableExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#typeExpression.
    def visitTypeExpression(self, ctx:vbaParser.TypeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#definedTypeExpression.
    def visitDefinedTypeExpression(self, ctx:vbaParser.DefinedTypeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#addressofExpression.
    def visitAddressofExpression(self, ctx:vbaParser.AddressofExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#procedurePointerExpression.
    def visitProcedurePointerExpression(self, ctx:vbaParser.ProcedurePointerExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#wsc.
    def visitWsc(self, ctx:vbaParser.WscContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#endOfLine.
    def visitEndOfLine(self, ctx:vbaParser.EndOfLineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#endOfLineNoWs.
    def visitEndOfLineNoWs(self, ctx:vbaParser.EndOfLineNoWsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#endOfStatement.
    def visitEndOfStatement(self, ctx:vbaParser.EndOfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#endOfStatementNoWs.
    def visitEndOfStatementNoWs(self, ctx:vbaParser.EndOfStatementNoWsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#commentBody.
    def visitCommentBody(self, ctx:vbaParser.CommentBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#reservedIdentifier.
    def visitReservedIdentifier(self, ctx:vbaParser.ReservedIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#ambiguousIdentifier.
    def visitAmbiguousIdentifier(self, ctx:vbaParser.AmbiguousIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#statementKeyword.
    def visitStatementKeyword(self, ctx:vbaParser.StatementKeywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#remKeyword.
    def visitRemKeyword(self, ctx:vbaParser.RemKeywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#markerKeyword.
    def visitMarkerKeyword(self, ctx:vbaParser.MarkerKeywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#operatorIdentifier.
    def visitOperatorIdentifier(self, ctx:vbaParser.OperatorIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#reservedName.
    def visitReservedName(self, ctx:vbaParser.ReservedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#specialForm.
    def visitSpecialForm(self, ctx:vbaParser.SpecialFormContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#reservedTypeIdentifier.
    def visitReservedTypeIdentifier(self, ctx:vbaParser.ReservedTypeIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#typeableReservedName.
    def visitTypeableReservedName(self, ctx:vbaParser.TypeableReservedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#literalIdentifier.
    def visitLiteralIdentifier(self, ctx:vbaParser.LiteralIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#booleanLiteralIdentifier.
    def visitBooleanLiteralIdentifier(self, ctx:vbaParser.BooleanLiteralIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#objectLiteralIdentifier.
    def visitObjectLiteralIdentifier(self, ctx:vbaParser.ObjectLiteralIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#variantLiteralIdentifier.
    def visitVariantLiteralIdentifier(self, ctx:vbaParser.VariantLiteralIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#reservedForImplementationUse.
    def visitReservedForImplementationUse(self, ctx:vbaParser.ReservedForImplementationUseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#futureReserved.
    def visitFutureReserved(self, ctx:vbaParser.FutureReservedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#foreignName.
    def visitForeignName(self, ctx:vbaParser.ForeignNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#foreignIdentifier.
    def visitForeignIdentifier(self, ctx:vbaParser.ForeignIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#builtinType.
    def visitBuiltinType(self, ctx:vbaParser.BuiltinTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#typedName.
    def visitTypedName(self, ctx:vbaParser.TypedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#typeSuffix.
    def visitTypeSuffix(self, ctx:vbaParser.TypeSuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vbaParser#ambiguousKeyword.
    def visitAmbiguousKeyword(self, ctx:vbaParser.AmbiguousKeywordContext):
        return self.visitChildren(ctx)



del vbaParser
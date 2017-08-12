from .ast import Node

# ------------------------------------------------------------------------------
SEPERATOR = "\r\n"

class CompilationUnit(Node):
    attrs = ("package", "imports", "types")
    
    def to_java(self):
        package_str = self.package.to_java()
        imports = SEPERATOR.join([i.to_java() for i in self.imports])
        types = SEPERATOR.join([i.to_java() for i in self.types])
        value = package_str + SEPERATOR*2 + imports + SEPERATOR*2 + types

        return value

class Import(Node):
    attrs = ("path", "static", "wildcard")

    def to_java(self):
        value = 'import '
        if self.static:
            value = value + 'static '
        value = value + self.path
        if self.wildcard:
            value = value + '.*'
        value = value + ';'
        return value

class Documented(Node):
    attrs = ("documentation",)

class Declaration(Node):
    attrs = ("modifiers", "annotations")
    
    # TODO: consider order or the modifiers
    @property
    def modifiers_str(self):
        if self.modifiers:
            return " ".join(self.modifiers)+" "
        else:
            return ""

class TypeDeclaration(Declaration, Documented):
    attrs = ("name", "body")

    @property
    def fields(self):
        return [decl for decl in self.body if isinstance(decl, FieldDeclaration)]

    @property
    def methods(self):
        return [decl for decl in self.body if isinstance(decl, MethodDeclaration)]

    @property
    def constructors(self):
        return [decl for decl in self.body if isinstance(decl, ConstructorDeclaration)]

class PackageDeclaration(Declaration, Documented):
    attrs = ("name",)

    def to_java(self):
        name = self.name
        value = self.modifiers_str + 'package '+ name +';'
        return value

class ClassDeclaration(TypeDeclaration):
    attrs = ("type_parameters", "extends", "implements")

    def to_java(self):
        name = self.name 
        extends = self.extends
        implements = self.implements 
        # TODO:Implement this
        type_parameters = self.type_parameters
        body = [node.to_java() for node in self.body]
        
        adding_ext = ""
        if extends:
            adding_ext = " extends "+ extends.to_java()

        adding_imp = ""
        if implements:
            adding_imp = " implements " + ", ".join([t.to_java() for t in implements])

        value = self.modifiers_str + "class " +name+adding_ext+adding_imp
        
        value += "{"+SEPERATOR+SEPERATOR.join(body)+SEPERATOR+"}"
        return value

class EnumDeclaration(TypeDeclaration):
    attrs = ("implements",)

class InterfaceDeclaration(TypeDeclaration):
    attrs = ("type_parameters", "extends",)

class AnnotationDeclaration(TypeDeclaration):
    attrs = ()

# ------------------------------------------------------------------------------

class Type(Node):
    attrs = ("name", "dimensions",)

    @property
    def name_with_dimensions_str(self):
        return self.name+"[]"*len(self.dimensions)

    def to_java(self):
        return self.name_with_dimensions_str

class BasicType(Type):
    attrs = ()

    def to_java(self):
        return self.name_with_dimensions_str

class ReferenceType(Type):
    attrs = ("arguments", "sub_type")

    def to_java(self):
        #TODO: Implement this
        arguments = self.arguments
        sub_type = self.sub_type

        return self.name_with_dimensions_str 

class TypeArgument(Node):
    attrs = ("type", "pattern_type")

# ------------------------------------------------------------------------------

class TypeParameter(Node):
    attrs = ("name", "extends")

# ------------------------------------------------------------------------------

class Annotation(Node):
    attrs = ("name", "element")

class ElementValuePair(Node):
    attrs = ("name", "value")

class ElementArrayValue(Node):
    attrs = ("values",)

# ------------------------------------------------------------------------------

class Member(Documented):
    attrs = ()

class MethodDeclaration(Member, Declaration):
    attrs = ("type_parameters", "return_type", "name", "parameters", "throws", "body")

    @property
    def parameters_str(self):
        if self.parameters:
            paras = []
            for para in self.parameters:
                paras.append(para.to_java())

            return ", ".join(paras)
        else:
            return ""

    def to_java(self):
        name_str = self.name
        parameters_str = self.parameters_str
        modifiers_str = self.modifiers_str
        return_type_str = self.return_type.to_java()

        body = [node.to_java() for node in self.body]

        # TODO: Implement these
        type_parameters = self.type_parameters
        throws = self.throws

        value = modifiers_str+return_type_str+" "+name_str+"("+parameters_str+")"

        value += SEPERATOR + "{" + SEPERATOR + SEPERATOR.join(body) + SEPERATOR+"}"
        return value

class FieldDeclaration(Member, Declaration):
    attrs = ("type", "declarators")

class ConstructorDeclaration(Declaration, Documented):
    attrs = ("type_parameters", "name", "parameters", "throws", "body")

# ------------------------------------------------------------------------------

class ConstantDeclaration(FieldDeclaration):
    attrs = ()

class ArrayInitializer(Node):
    attrs = ("initializers",)

class VariableDeclaration(Declaration):
    attrs = ("type", "declarators")

class LocalVariableDeclaration(VariableDeclaration):
    attrs = ()

class VariableDeclarator(Node):
    attrs = ("name", "dimensions", "initializer")

class FormalParameter(Declaration):
    attrs = ("type", "name", "varargs")
    
    def to_java(self):
        type_str = self.type.to_java()
        value = self.modifiers_str+type_str+' '+self.name
        return value

class InferredFormalParameter(Node):
    attrs = ('name',)

# ------------------------------------------------------------------------------

class Statement(Node):
    attrs = ("label",)

class IfStatement(Statement):
    attrs = ("condition", "then_statement", "else_statement")

class WhileStatement(Statement):
    attrs = ("condition", "body")

class DoStatement(Statement):
    attrs = ("condition", "body")

class ForStatement(Statement):
    attrs = ("control", "body")

class AssertStatement(Statement):
    attrs = ("condition", "value")

class BreakStatement(Statement):
    attrs = ("goto",)

class ContinueStatement(Statement):
    attrs = ("goto",)

class ReturnStatement(Statement):
    attrs = ("expression",)

class ThrowStatement(Statement):
    attrs = ("expression",)

class SynchronizedStatement(Statement):
    attrs = ("lock", "block")

class TryStatement(Statement):
    attrs = ("resources", "block", "catches", "finally_block")

class SwitchStatement(Statement):
    attrs = ("expression", "cases")

class BlockStatement(Statement):
    attrs = ("statements",)

class StatementExpression(Statement):
    attrs = ("expression",)

# ------------------------------------------------------------------------------

class TryResource(Declaration):
    attrs = ("type", "name", "value")

class CatchClause(Statement):
    attrs = ("parameter", "block")

class CatchClauseParameter(Declaration):
    attrs = ("types", "name")

# ------------------------------------------------------------------------------

class SwitchStatementCase(Node):
    attrs = ("case", "statements")

class ForControl(Node):
    attrs = ("init", "condition", "update")

class EnhancedForControl(Node):
    attrs = ("var", "iterable")

# ------------------------------------------------------------------------------

class Expression(Node):
    attrs = ()

class Assignment(Expression):
    attrs = ("expressionl", "value", "type")

class TernaryExpression(Expression):
    attrs = ("condition", "if_true", "if_false")

class BinaryOperation(Expression):
    attrs = ("operator", "operandl", "operandr")

class Cast(Expression):
    attrs = ("type", "expression")

class MethodReference(Expression):
    attrs = ("expression", "method", "type_arguments")

class LambdaExpression(Expression):
    attrs = ('parameters', 'body')

# ------------------------------------------------------------------------------

class Primary(Expression):
    attrs = ("prefix_operators", "postfix_operators", "qualifier", "selectors")

class Literal(Primary):
    attrs = ("value",)

class This(Primary):
    attrs = ()

class MemberReference(Primary):
    attrs = ("member",)

class Invocation(Primary):
    attrs = ("type_arguments", "arguments")

class ExplicitConstructorInvocation(Invocation):
    attrs = ()

class SuperConstructorInvocation(Invocation):
    attrs = ()

class MethodInvocation(Invocation):
    attrs = ("member",)

class SuperMethodInvocation(Invocation):
    attrs = ("member",)

class SuperMemberReference(Primary):
    attrs = ("member",)

class ArraySelector(Expression):
    attrs = ("index",)

class ClassReference(Primary):
    attrs = ("type",)

class VoidClassReference(ClassReference):
    attrs = ()

# ------------------------------------------------------------------------------

class Creator(Primary):
    attrs = ("type",)

class ArrayCreator(Creator):
    attrs = ("dimensions", "initializer")

class ClassCreator(Creator):
    attrs = ("constructor_type_arguments", "arguments", "body")

class InnerClassCreator(Creator):
    attrs = ("constructor_type_arguments", "arguments", "body")

# ------------------------------------------------------------------------------

class EnumBody(Node):
    attrs = ("constants", "declarations")

class EnumConstantDeclaration(Declaration, Documented):
    attrs = ("name", "arguments", "body")

class AnnotationMethod(Declaration):
    attrs = ("name", "return_type", "dimensions", "default")

from .ast import Node

# ------------------------------------------------------------------------------
SEPERATOR = "\r\n"

class CompilationUnit(Node):
    """
        package: Node - PackageDeclaration
        imports: Node - Import
        types:  List of Node
    """
    attrs = ("package", "imports", "types")
    
    def to_java(self):
        package_str = self.package.to_java()
        imports = SEPERATOR.join([i.to_java() for i in self.imports])
        types = SEPERATOR.join([i.to_java() for i in self.types])
        value = package_str + SEPERATOR*2 + imports + SEPERATOR*2 + types

        return value

class Import(Node):
    """
        path: String of import path
        static: Boolean of whether add static
        wildcard: Boolean of whether add ".*"
    """
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
    """
        documentation: String of documentation
    """
    attrs = ("documentation",)

class Declaration(Node):
    """
        modifers: List of String (of modifiers)
        annotations: List of Node — AnnotationDeclaration
    """
    attrs = ("modifiers", "annotations")
    
    # TODO: consider order or the modifiers
    @property
    def modifiers_str(self):
        if self.modifiers:
            return " ".join(self.modifiers)+" "
        else:
            return ""

    @property
    def annotations_str(self):
        annotations = ['@'+i.name for i in self.annotations] #TODO: self.elements
        return SEPERATOR.join(annotations)+SEPERATOR

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

        value = self.annotations_str + self.modifiers_str + "class " +name+adding_ext+adding_imp
        value += SEPERATOR+"{"+SEPERATOR+SEPERATOR.join(body)+SEPERATOR+"}"
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
    def name_and_dimensions_str(self):
        return get_name_and_dimensions_str(self)

    def to_java(self):
        return self.name_and_dimensions_str

class BasicType(Type):
    attrs = ()

    def to_java(self):
        return self.name_and_dimensions_str

class ReferenceType(Type):
    attrs = ("arguments", "sub_type")

    def to_java(self):
        #TODO: Implement this
        arguments = self.arguments
        sub_type = self.sub_type

        return self.name_and_dimensions_str 

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
        return get_parameter_str(self)

    def to_java(self):
        name_str = self.name
        parameters_str = self.parameters_str
        modifiers_str = self.modifiers_str
        return_type_str = self.return_type.to_java()

        body = [node.to_java() for node in self.body]

        # TODO: Implement these
        type_parameters = self.type_parameters
        throws = self.throws

        value = self.annotations_str + modifiers_str+return_type_str+" "+name_str+"("+parameters_str+")"

        value += "{" +  SEPERATOR + SEPERATOR.join(body) + SEPERATOR+"}"
        return value

class FieldDeclaration(Member, Declaration):
    attrs = ("type", "declarators")

    def to_java(self):
        modifiers_str = self.modifiers_str
        type_str = self.type.to_java()

        declarators = [i.to_java() for i in self.declarators]

        value = self.annotations_str + modifiers_str+type_str+" "
        value += ", ".join(declarators)
        value += ";"
        
        return value

class ConstructorDeclaration(Declaration, Documented):
    attrs = ("type_parameters", "name", "parameters", "throws", "body")

    def to_java(self):
        modifiers_str = self.modifiers_str
        name_str = self.name
        parameters_str = get_parameter_str(self)

        body = [i.to_java() for i in self.body]

        value = self.annotations_str + modifiers_str+name_str+'('+parameters_str+')'
        value += " {" + SEPERATOR + SEPERATOR.join(body) + SEPERATOR+"}"
        return value
        
# ------------------------------------------------------------------------------

class ConstantDeclaration(FieldDeclaration):
    attrs = ()

class ArrayInitializer(Node):
    attrs = ("initializers",)

    def to_java(self):
        initialzers = [i.to_java() for i in self.initializers]

        value = "{" + ", ".join(initialzers) + "}"

        return value

class VariableDeclaration(Declaration):
    attrs = ("type", "declarators")

class LocalVariableDeclaration(VariableDeclaration):
    attrs = ()

class VariableDeclarator(Node):
    attrs = ("name", "dimensions", "initializer")

    def to_java(self):
        name_and_dimensions_str = get_name_and_dimensions_str(self)
        value = name_and_dimensions_str
        if self.initializer:
            initializer_str = self.initializer.to_java()
            value += ' = '+initializer_str

        return value

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
    
    def to_java(self):
        expression_str = self.expression.to_java()

        ret = "return "+expression_str+";"

        return ret

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

    def to_java(self):
        label = self.label #TODO:?
        expression_str = self.expression.to_java()
        
        ret = expression_str+";"
        return ret

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

    def to_java(self):
        expressionl_str = self.expressionl.to_java()
        value_str = self.value.to_java()
        type_str = self.type

        ret = expressionl_str+' '+type_str+' '+value_str
        return ret

class TernaryExpression(Expression):
    attrs = ("condition", "if_true", "if_false")

class BinaryOperation(Expression):
    attrs = ("operator", "operandl", "operandr")

    def to_java(self):
        operator_str = self.operator
        operandl_str = self.operandl.to_java()
        operandr_str = self.operandr.to_java()

        value =  operandl_str + ' ' + operator_str + ' ' +operandr_str
        return value

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

    def to_java(self):
        value_str = self.value
        
        return value_str

class This(Primary):
    attrs = ()

    def to_java(self):
        return "this"

class MemberReference(Primary):
    attrs = ("member",)

    def to_java(self):
        member_str = self.member
        qualifier_str = self.qualifier

        #TODO:preflix, postflix,selector 
        if qualifier_str:
            value = qualifier_str+'.'+member_str
        else:
            value = member_str 
        return value

class Invocation(Primary):
    attrs = ("type_arguments", "arguments")

class ExplicitConstructorInvocation(Invocation):
    attrs = ()

class SuperConstructorInvocation(Invocation):
    attrs = ()

    def to_java(self):
        arguments = [i.to_java() for i in self.arguments]
        value = "super("+ SEPERATOR.join(arguments) + ")"

        return value

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

    def to_java(self):
        type_str = self.type.to_java()
        value = "new "+type_str
        return value

class ArrayCreator(Creator):
    attrs = ("dimensions", "initializer")

    def to_java(self):
        type_str = self.type.to_java()
        type_and_dimension_str = get_name_and_dimensions_str_bare(type_str, self.dimensions)
        if self.initializer:
            initializer_str = self.initializer.to_java()
        else:
            initializer_str = ""

        value = "new "+type_and_dimension_str+initializer_str

        return value


class ClassCreator(Creator):
    attrs = ("constructor_type_arguments", "arguments", "body")

    def to_java(self):
        type_str = self.type.to_java()

        if self.body != None:
            body = [i.to_java() for i in self.body]
            body_str = "{" + SEPERATOR.join(body) + "}"
        else:
            body_str = ""

        arguments = [i.to_java() for i in self.arguments]
        arguments_str = ", ".join(arguments)
        
        value = "new "+type_str+"("+arguments_str+")"+body_str
        return value

class InnerClassCreator(Creator):
    attrs = ("constructor_type_arguments", "arguments", "body")

# ------------------------------------------------------------------------------

class EnumBody(Node):
    attrs = ("constants", "declarations")

class EnumConstantDeclaration(Declaration, Documented):
    attrs = ("name", "arguments", "body")

class AnnotationMethod(Declaration):
    attrs = ("name", "return_type", "dimensions", "default")


def get_name_and_dimensions_str_bare(name, dimensions):
    ret = name
    for i in dimensions:
        if i:
            ret += "["+i.to_java()+"]"
        else:
            ret += "[]"
        
    return ret

#TODO: Modify dimension expansion
def get_name_and_dimensions_str(node):
    if not node.dimensions:
        return node.name
    return get_name_and_dimensions_str_bare(node.name, node.dimensions)

def get_parameter_str(node):
    if node.parameters:
        paras = []
        for para in node.parameters:
            paras.append(para.to_java())

        return ", ".join(paras)
    else:
        return ""

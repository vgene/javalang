        class CompilationUnit(Node):
        class Import(Node):
        class Documented(Node):
        class Declaration(Node):
        class TypeDeclaration(Declaration, Documented):
        class PackageDeclaration(Declaration, Documented):

    class ClassDeclaration(TypeDeclaration):
class EnumDeclaration(TypeDeclaration):
class InterfaceDeclaration(TypeDeclaration):
class AnnotationDeclaration(TypeDeclaration):
        class Type(Node):
        class BasicType(Type):
    class ReferenceType(Type):
class TypeArgument(Node):
class TypeParameter(Node):
    class Annotation(Node):
class ElementValuePair(Node):
class ElementArrayValue(Node):
class Member(Documented):
class MethodDeclaration(Member, Declaration):
class FieldDeclaration(Member, Declaration):
class ConstructorDeclaration(Declaration, Documented):
class ConstantDeclaration(FieldDeclaration):
class ArrayInitializer(Node):
class VariableDeclaration(Declaration):
class LocalVariableDeclaration(VariableDeclaration):
class VariableDeclarator(Node):
class FormalParameter(Declaration):
class InferredFormalParameter(Node):
class Statement(Node):
class IfStatement(Statement):
class WhileStatement(Statement):
class DoStatement(Statement):
class ForStatement(Statement):
class AssertStatement(Statement):
class BreakStatement(Statement):
class ContinueStatement(Statement):
class ReturnStatement(Statement):
class ThrowStatement(Statement):
class SynchronizedStatement(Statement):
class TryStatement(Statement):
class SwitchStatement(Statement):
class BlockStatement(Statement):
class StatementExpression(Statement):
class TryResource(Declaration):
class CatchClause(Statement):
class CatchClauseParameter(Declaration):
class SwitchStatementCase(Node):
class ForControl(Node):
class EnhancedForControl(Node):
class Expression(Node):
class Assignment(Expression):
class TernaryExpression(Expression):
class BinaryOperation(Expression):
class Cast(Expression):
class MethodReference(Expression):
class LambdaExpression(Expression):
class Primary(Expression):
class Literal(Primary):
class This(Primary):
class MemberReference(Primary):
class Invocation(Primary):
class ExplicitConstructorInvocation(Invocation):
class SuperConstructorInvocation(Invocation):
class MethodInvocation(Invocation):
class SuperMethodInvocation(Invocation):
class SuperMemberReference(Primary):
class ArraySelector(Expression):
class ClassReference(Primary):
class VoidClassReference(ClassReference):
class Creator(Primary):
class ArrayCreator(Creator):
class ClassCreator(Creator):
class InnerClassCreator(Creator):
class EnumBody(Node):
class EnumConstantDeclaration(Declaration, Documented):
class AnnotationMethod(Declaration):

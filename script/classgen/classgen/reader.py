import copy
from overrides import override
from classgen_grammarParser  import classgen_grammarParser
from classgen_grammarVisitor import classgen_grammarVisitor
from .             import tree            as cg_tree
from .reader_stack import cg_reader_stack as cg_reader_stack
    
#
#
#
class cg_reader_visitor(classgen_grammarVisitor):
  def __init__(self, parser):
    self.indentation               = 0
    self.parser                    = parser
    self.trunk:cg_tree.symbol_node = cg_tree.symbol_node(None, "trunk")
    self.stack:cg_reader_stack     = cg_reader_stack()
    self.stack.tail().symbol_node  = self.trunk
    
  #
  #
  #
  @override
  def visitDefinition_object(self, ctx:classgen_grammarParser.Definition_objectContext):
    new_node:cg_tree.symbol_node = self.open_node_from_path(ctx.identifier_ex())
    new_node.symbol_type = self.get_node_type_from_object_type(ctx.object_type())

    self.stack.push()
    self.stack.tail().symbol_node = new_node

    super().visitTranslation_unit_object(ctx)

    self.stack.pop()
    
  #
  #
  #
  @override
  def visitDefinition_object_constant(self, ctx:classgen_grammarParser.Definition_object_constantContext):
    new_node:cg_tree.symbol_node = self.open_node_from_path(ctx.identifier_ex())
    new_node.symbol_type = cg_tree.symbol_node_type.CONSTANT
    
  #
  #
  #
  @override
  def visitDefinition_object_body_square(self, ctx:classgen_grammarParser.Definition_object_body_squareContext):
    if self.stack.tail().symbol_node.symbol_type == cg_tree.symbol_node_type.TOKENS:
      return super().visitDefinition_object_body_square(ctx)

    new_node = self.push_node_token_object([ "~tokens" ])
    new_node.enter_secretly = True
    super().visitDefinition_object_body_square(ctx)
    self.stack.pop()
    
  #
  #
  #
  @override
  def visitDefinition_object_sbracket_list(self, ctx:classgen_grammarParser.Definition_object_sbracket_listContext):
    new_node = self.push_node_token_object([ "~tokens" ])
    new_node.enter_secretly = True
    super().visitDefinition_object_sbracket_list(ctx)
    self.stack.pop()

    
  #
  #
  #
  @override
  def visitDeclaration_object_implied_map(self, ctx:classgen_grammarParser.Declaration_object_implied_mapContext):
    new_node:cg_tree.symbol_node = self.open_node_from_path(ctx.identifier_ex())
    new_node.symbol_type = cg_tree.symbol_node_type.FN_MAP
    new_node.tags.append("impl_defined")

    self.stack.push()
    self.stack.tail().symbol_node = new_node
    
    super().visitDeclaration_object_implied_map(ctx)

    self.stack.pop()
    
  #
  #
  #
  def push_node_token_object(self, path:list[str]):
    new_node:cg_tree.symbol_node =self.stack.tail().symbol_node.resolve_path_with_create(path)
    new_node.symbol_type = cg_tree.symbol_node_type.TOKENS

    self.stack.push()
    self.stack.tail().symbol_node = new_node

    return new_node
    
  #
  #
  #
  def push_node_args_object(self, path:list[str]):
    new_node:cg_tree.symbol_node =self.stack.tail().symbol_node.resolve_path_with_create(path)
    new_node.symbol_type = cg_tree.symbol_node_type.ARGS

    self.stack.push()
    self.stack.tail().symbol_node = new_node

    
  #
  #
  #
  def open_node_from_path(self, ctx:classgen_grammarParser.Identifier_exContext):
    real_node = None

    if ctx.identifier_pure():
      name      = self.get_name_from_identifier_pure(ctx.identifier_pure())
      real_node = self.stack.tail().symbol_node.resolve_path_with_create(name)
    elif ctx.identifier_with_alias():
      alias_ctx = ctx.identifier_with_alias()
      name      = self.get_name_from_identifier_pure(alias_ctx.identifier_pure())
      real_node = self.stack.tail().symbol_node.resolve_path_with_create(name)
      alias_list_ctx = alias_ctx.identifier_alias_list()
      for elem in alias_list_ctx.identifier_name():
        alias_name = self.get_name_from_identifier_name(elem)
        node = self.stack.tail().symbol_node.resolve_path_with_create(alias_name)
        if node.change_to_type_or_fail(cg_tree.symbol_node_type.LOCAL_ALIAS):
          node.symbol_target = real_node
    else:
      name = [ "_ANONYMOUS_" ]

    return real_node
    
  #
  #
  #
  def get_name_from_identifier_name(self, ctx:classgen_grammarParser.Identifier_nameContext):
     name = ctx.identifier_id().getText()
     if ctx.identifier_namespace_pre():
       return [ ctx.identifier_namespace_pre().getText().split("::"), name ]
     return [ name ]
    
  #
  #
  #
  def get_name_from_identifier_pure(self, ctx:classgen_grammarParser.Identifier_pureContext):
     path = self.get_name_from_identifier_name(ctx.identifier_name())
     if ctx.identifier_postfix() and ctx.identifier_postfix().identifier_namespace_post():
       post_ctx = ctx.identifier_postfix().identifier_namespace_post()
       path = post_ctx.identifier_namespace_list().getText().split("::") + path
     return path
    
  #
  #
  #
  def get_node_type_from_object_type(self, ctx:classgen_grammarParser.Object_typeContext):
    match (ctx.t.type):
      case self.parser.TYPEWORD_REFL:
        return cg_tree.symbol_node_type.REFL
      case self.parser.TYPEWORD_ENUM:
        return cg_tree.symbol_node_type.ENUM
      case self.parser.TYPEWORD_POD:
        return cg_tree.symbol_node_type.POD
      case self.parser.TYPEWORD_PROC:
        return cg_tree.symbol_node_type.PROC
      case self.parser.TYPEWORD_TOKENS:
        return cg_tree.symbol_node_type.TOKENS
      case _:
        print("errr")
        return cg_tree.symbol_node_type.NONE

    
  #
  #
  #
  def visitChildren(self, ctx):
    #print(('  ' * self.indentation) + self.parser.ruleNames[ctx.getRuleIndex()])
    self.indentation += 1
    super().visitChildren(ctx)
    self.indentation -= 1
    
  def visitTerminal(self, ctx):
    #print(('  ' * self.indentation) + '"' + ctx.getText() + '"')
    super().visitTerminal(ctx)
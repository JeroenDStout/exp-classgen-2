import copy
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
  def visitDefinition_object(self, ctx:classgen_grammarParser.Definition_objectContext):
    new_node:cg_tree.symbol_node = self.stack.tail().symbol_node.resolve_path_with_create(ctx.identifier_ex().getText().split("::"))

    self.stack.push()
    self.stack.tail().symbol_node = new_node

    super().visitTranslation_unit_object(ctx)

    self.stack.pop()
    
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
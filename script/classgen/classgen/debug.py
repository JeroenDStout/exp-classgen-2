from classgen_grammarVisitor import classgen_grammarVisitor

class classgen_debug_visitor(classgen_grammarVisitor):
  def __init__(self, parser):
    self.parser     = parser
    self.identation = 0
    
  def visitChildren(self, ctx):
    print(('  ' * self.identation) + self.parser.ruleNames[ctx.getRuleIndex()])
    self.identation += 1
    super().visitChildren(ctx)
    self.identation -= 1
    
  def visitTerminal(self, ctx):
    print(('  ' * self.identation) + '"' + ctx.getText() + '"')
    super().visitTerminal(ctx)
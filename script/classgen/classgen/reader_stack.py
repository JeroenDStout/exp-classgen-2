import copy
from . import tree as cg_tree
  
#
#
#
class cg_reader_stack():
  class cg_context():
    def __init__(self):
      self.symbol_node:cg_tree.symbol_node = None
      
    def __str__(self):
      ret = "cg_context"
      if self.symbol_node:
        ret += "\nnode: " + str(self.symbol_node)
      return ret

  def __init__(self):
    context = self.cg_context()
    self.context_stack  = [ context ]
      
  def __str__(self):
    ret = "cg_reader_stack"
    idx = 0
    for elem in self.context_stack:
      ret += "\n[" + str(idx) + "] " + str(elem).replace("\n", "\n  ")
      idx += 1
    return ret
  
  def tail(self):
    return self.context_stack[-1]
  
  def push(self):
    self.context_stack.append(copy.copy(self.context_stack[-1]))
  
  def pop(self):
    self.context_stack.pop()
import copy
from enum import Enum, auto
from os   import path as os_path
from .    import tree as cg_tree

#
#
#
class cg_writer():
  #
  class visit_type(Enum):
    NONE  = auto()
    ENTER = auto()
    WRITE = auto()
    
  #
  class meta_symbol_type(Enum):
    INDENT         = auto()
    COMMENT        = auto()
    OPTIONAL_SPACE = auto()
    OPTIONAL_COMMA = auto()
    
  #
  #
  #
  class meta_symbol():
    def __init__(self, symbol_type, value):
      self.type  = symbol_type
      self.value = value

  #
  #
  #
  def __init__(self, trunk:cg_tree.symbol_node):
    self.trunk:cg_tree.symbol_node = trunk
    self.current_visit_stack       = [ trunk ]
    
  def write(self, out_path:str):
    content = []
    content += self.write_intro()
    content += self.write_visit(self.trunk)
    self.write_if_updated(out_path, content)

  def get_visit_type(self, node:cg_tree.symbol_node):
    return self.visit_type.ENTER;

  def write_intro(self):
    return []

  def write_visit_with_stack(self, node:cg_tree.symbol_node):
    ret = self.write_visit(node)
    if self.current_visit_stack[-1] == node:
      ret += self.write_visit_leave(node)
      self.current_visit_stack.pop()
    return ret

  def write_visit(self, node:cg_tree.symbol_node):
    visit_type = self.get_visit_type(node)

    if visit_type == self.visit_type.NONE:
      return []

    if visit_type == self.visit_type.ENTER:
      ret = []
      for elem in node.children:
        ret += self.write_visit_with_stack(elem)
      return ret
      
    ret = self.write_visit_specific(node)
    if len(ret) > 0:
      return self.write_visit_enter_with_stack(node.parent) + ret

    return []

  def write_visit_enter_with_stack(self, node:cg_tree.symbol_node):    
    if self.current_visit_stack[-1] == node:
      return []
      
    ret = self.write_visit_enter_with_stack(node.parent)

    self.current_visit_stack.append(node)
    return ret + self.write_visit_enter(node)

  def write_visit_enter(self, node:cg_tree.symbol_node):
    return []

  def write_visit_leave(self, node:cg_tree.symbol_node):
    return []

  def write_visit_specific(self, node:cg_tree.symbol_node):
    return []

  def write_if_updated(self, out_path:str, contents:list[str]):
    string = ""

    newline = False
    indentation = 0
    comment     = 0
    optional_space_count = 0
    optional_comma_count = 0

    for elem in contents:
      if isinstance(elem, str):
        if optional_comma_count > 1:
          string += ","
        if optional_space_count > 1:
          string += "\n" + " " * indentation
        optional_space_count = 0
        optional_comma_count = 0

        if newline:
          string += "\n"
        newline = True

        current_indent = max(0, indentation - (comment * 2))
        string += ("//" * comment) + (" " * current_indent) + elem

      elif isinstance(elem, self.meta_symbol):
        match elem.type:
          case self.meta_symbol_type.INDENT:
            indentation += elem.value
          case self.meta_symbol_type.COMMENT:
            comment += elem.value
          case self.meta_symbol_type.OPTIONAL_SPACE:
            optional_space_count += 1
          case self.meta_symbol_type.OPTIONAL_COMMA:
            optional_comma_count += 1

    string += "\n"

    # debug
    #print(string)
    
    if os_path.isfile(out_path):
      with open(out_path, 'r') as old_file:
        old_content = old_file.read()
        if old_content == string:
          print(f"* ({os_path.basename(out_path)} was up to date)")
          return          
          
    with open(out_path, 'w') as new_file:
      new_file.write(string)
      
    print(f"* {os_path.basename(out_path)} updated")
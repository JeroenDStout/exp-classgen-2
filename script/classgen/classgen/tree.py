from __future__ import annotations
from enum import Enum, auto
import copy

#
#
#
class symbol_node_type(Enum):
  NONE         = auto()
  ALIAS        = auto()
  ALIAS_LOCAL  = auto()
  NAMESPACE    = auto()
  REFL         = auto()
  LINK         = auto()
  ENUM         = auto()
  POD          = auto()
  PROC         = auto()
  TOKENS       = auto()
  ARGS         = auto()
  FN_MAP       = auto()
  CONSTANT     = auto()
  
class symbol_node():
  def __init__(self, parent_, identifier_:str):
    self.identifier:str               = identifier_
    self.payload                      = None
    self.tags:list[str]               = []
    self.symbol_type:symbol_node_type = symbol_node_type.NONE
    self.enter_secretly:bool          = False

    self.parent:symbol_node           = parent_
    self.symbol_target:symbol_node    = None
    self.children:list[symbol_node]   = []
    self.dangling_objects:list        = []

  def copy_very_shallow(self, parent):
    ret = symbol_node(parent, self.identifier)
    ret.identifier     = self.identifier
    ret.tags           = copy.copy(self.tags)
    ret.symbol_type    = self.symbol_type
    ret.enter_secretly = self.enter_secretly
    return ret
  
  def to_big_string(self):
    ret = "[" + self.symbol_type.name + "] " + self.identifier
    if len(self.tags) > 0:
      ret += " <" + ", ".join(self.tags) + ">"
    if self.symbol_target:
      symbol = self.symbol_target
      while symbol:
        ret += "\n  @ ::" + "::".join(symbol.get_canonical_path())
        symbol = symbol.symbol_target
    if self.payload:
      ret += "\n  # " + str(self.payload).replace("\n", "\n  ")
    for obj in self.dangling_objects:
      ret += "\n  ~ " + str(obj).replace("\n", "\n  ")
    for child in self.children:
      ret += "\n- " + child.to_big_string().replace("\n", "\n  ")
    return ret

  def add_child(self, identifier:str):
    node:symbol_node = symbol_node(self, identifier)
    self.children.append(node)
    return node

  def get_canonical_path(self):
    if not self.parent:
      return []
    return self.parent.get_canonical_path() + [ self.identifier ]

  #
  #
  #
  def resolve_path(self, path_name:list[str], follow_alias_local=True):
    if self.symbol_type == symbol_node_type.ALIAS:
      return self.symbol_target.resolve_path(path_name, follow_alias_local)
    if follow_alias_local and self.symbol_type == symbol_node_type.ALIAS_LOCAL:
      return self.symbol_target.resolve_path(path_name, follow_alias_local)

    if len(path_name) == 0:
      return self

    if path_name[0] == "..":
      return self.parent.resolve_path(path_name[1:], False)

    for child in self.children:
      if path_name[0] == child.identifier:
        return child.resolve_path(path_name[1:], False)
      if child.enter_secretly:
        result = child.resolve_path(path_name, False)
        if result:
          return result
          
    return self.parent.resolve_path(path_name, follow_alias_local)
    
  #
  #
  #
  def resolve_path_with_create(self, path_name:list[str]):
    if len(path_name) == 0:
      return self

    if path_name[0] == "..":
      return self.parent.resolve_path_with_create(path_name[1:])

    for child in self.children:
      if path_name[0] == child.identifier:
        return child.resolve_path_with_create(path_name[1:])

    return self.add_child(path_name[0]).resolve_path_with_create(path_name[1:])
    
  #
  #
  #
  def change_to_type_or_fail(self, symbol_type:symbol_node_type):
    if self.symbol_type == symbol_type:
      return True
    if self.symbol_type == symbol_node_type.NONE:
      self.symbol_type = symbol_type
      return True
    print ("ERRR")
    return False
  

class visit_symbol_nodes:
  def __iter__(self, starting_node):
    self.stack = [[starting_node, -1]]
    return self

  def __next__(self):
    last_elem = self.stack[-1]
    if last_elem[1] == -1:
      last_elem[1] += 1
      return last_elem[0]
    
    while len(last_elem[0].children) <= last_elem[1]:
      if len(self.stack) == 1:
        raise StopIteration
      
      self.stack.pop()
      last_elem = self.stack[-1]

    next_node = last_elem[0].children[last_elem[1]]
    last_elem[1] += 1
      
    return next_node
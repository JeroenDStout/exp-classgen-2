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
  FN           = auto()
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
  
  def ensure_child(self, identifier:str):
    return self.resolve_path_with_create([ identifier ])
  
  def remove_child(self, child:symbol_node):
    self.children.remove(child)
  
  def change_parent(self, new_parent:symbol_node):
    if self.parent:
      self.parent.remove_child(self)
    new_parent.children.append(self)
    self.parent = new_parent

  def get_canonical_path(self):
    if not self.parent:
      return []
    return self.parent.get_canonical_path() + [ self.identifier ]

  #
  #
  #
  def resolve_path(self, path_name:list[str], follow_alias_local=True, allow_auto_parent=True):
    if self.symbol_type == symbol_node_type.ALIAS:
      return self.symbol_target.resolve_path(path_name, follow_alias_local, allow_auto_parent)
    if follow_alias_local and self.symbol_type == symbol_node_type.ALIAS_LOCAL:
      return self.symbol_target.resolve_path(path_name, follow_alias_local, allow_auto_parent)

    if len(path_name) == 0:
      return self

    if path_name[0] == "..":
      return self.parent.resolve_path(path_name[1:], False, allow_auto_parent)

    for child in self.children:
      if path_name[0] == child.identifier:
        return child.resolve_path(path_name[1:], False, False)
      if child.enter_secretly:
        result = child.resolve_path(path_name, False, False)
        if result:
          return result
          
    if not allow_auto_parent:
      return None

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
    
  #
  #
  #
  def add_nodes_to_list_recursively(self, ref_list:list[symbol_node]):
    ref_list.append(self)
    for child in self.children:
      child.add_nodes_to_list_recursively(ref_list)
  

def visit_symbol_nodes(starting_node:symbol_node):
  yield starting_node
  for child in starting_node.children:
    yield from visit_symbol_nodes(child)
from __future__ import annotations
from enum import Enum

#
#
#
class symbol_node_type(Enum):
  NONE      = 0
  NAMESPACE = 1
  REFL      = 2
  ENUM      = 3
  POD       = 4
  PROC      = 5
  
class symbol_node():
  def __init__(self, parent_, identifier_:str):
    self.identifier:str               = identifier_
    self.payload                      = None
    self.tags:list[str]               = []

    self.parent:symbol_node           = parent_
    self.symbol_type:symbol_node_type = symbol_node_type.NONE
    self.symbol_target:symbol_node    = None
    self.children:list[symbol_node]   = []
  
  def to_big_string(self):
    ret = self.identifier
    if self.payload:
      ret += "\n# " + str(self.payload).replace("\n", "\n  ")
    for child in self.children:
      ret += "\n- " + child.to_big_string().replace("\n", "\n  ")
    return ret

  def add_child(self, identifier:str) -> symbol_node:
    node:symbol_node = symbol_node(self, identifier)
    self.children.append(node)
    return node

  def resolve_path_with_create(self, path_name:list[str]) -> symbol_node:
    if len(path_name) == 0:
      return self

    if path_name[0] == "..":
      return self.parent.resolve_path_with_create(path_name[1:])

    for child in self.children:
      if path_name[0] == child.identifier:
        return child.resolve_path_with_create(path_name[1:])

    return self.add_child(path_name[0]).resolve_path_with_create(path_name[1:])
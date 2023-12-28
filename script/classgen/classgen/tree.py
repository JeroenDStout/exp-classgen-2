from __future__ import annotations
from enum import Enum, auto

#
#
#
class symbol_node_type(Enum):
  NONE        = auto()
  LOCAL_ALIAS = auto()
  NAMESPACE   = auto()
  REFL        = auto()
  ENUM        = auto()
  POD         = auto()
  PROC        = auto()
  TOKENS      = auto()
  ARGS        = auto()
  FN_MAP      = auto()
  CONSTANT    = auto()
  
class symbol_node():
  def __init__(self, parent_, identifier_:str):
    self.identifier:str               = identifier_
    self.payload                      = None
    self.tags:list[str]               = []

    self.parent:symbol_node           = parent_
    self.symbol_type:symbol_node_type = symbol_node_type.NONE
    self.symbol_target:symbol_node    = None
    self.children:list[symbol_node]   = []
    self.enter_secretly:bool          = False
    self.dangling_objects:list        = []
  
  def to_big_string(self):
    ret = "[" + self.symbol_type.name + "] " + self.identifier
    if len(self.tags) > 0:
      ret += " <" + ",".join(self.tags) + ">"
    if self.symbol_target:
      ret += "\n  @ ::" + "::".join(self.symbol_target.get_canonical_path())
    if self.payload:
      ret += "\n  # " + str(self.payload).replace("\n", "\n  ")
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
  def resolve_path(self, path_name:list[str]):
    if len(path_name) == 0:
      return self

    if path_name[0] == "..":
      return self.parent.resolve_path(path_name[1:])

    for child in self.children:
      if path_name[0] == child.identifier:
        return child.resolve_path_with_create(path_name[1:])
      if child.enter_secretly:
        result = child.resolve_path(path_name)
        if result:
          return result

    return None
    
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
from enum import Enum, auto

class cg_typed_value_type(Enum):
  NONE      = auto()
  INTRINSIC = auto()
  CONSTANT  = auto()
  OBJECT    = auto()
  PATH      = auto()
  AUTO      = auto()

#
#
#
class cg_typed_value:
  def __init__(self):
    self.type_t:cg_typed_value_type    = cg_typed_value_type.NONE
    self.content_t:cg_typed_value_type = cg_typed_value_type.NONE
    self.content = None
    
  def __str__(self):
    ret = "<"

    ret += self.type_t.name
    ret += " "

    if self.content_t == cg_typed_value_type.OBJECT:
      ret += "@" + "::".join(self.content.get_canonical_path())
    elif self.content_t == cg_typed_value_type.PATH:
      ret += "$" + "::".join(self.content)
    elif self.content_t == cg_typed_value_type.CONSTANT:
      ret += str(self.content)
    else:
      ret += self.content_t.name

    ret += ">"
  
    return ret
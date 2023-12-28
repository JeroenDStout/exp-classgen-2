from .types_abstract import cg_typed_value, cg_typed_value_type

class cg_map_case:
  def __init__(self):
    self.src:cg_typed_value = cg_typed_value()
    self.dest:cg_typed_value  = cg_typed_value()

  def __str__(self):
    return "[" + str(self.src) + " -> " + str(self.dest) + "]"
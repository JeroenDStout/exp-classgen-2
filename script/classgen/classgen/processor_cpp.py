import copy
from .               import tree            as cg_tree
from .processor      import cg_processor
from .reader_stack   import cg_reader_stack
from .types_abstract import cg_typed_value
from .types_abstract import cg_typed_value_type
from .types_builtin  import cg_map_case

class cg_processor_cpp(cg_processor):
  def __init__(self, trunk:cg_tree.symbol_node):
    super().__init__(trunk)
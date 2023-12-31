from overrides import override
from .               import tree            as cg_tree
from .processor      import cg_processor
from .reader_stack   import cg_reader_stack
from .types_abstract import cg_typed_value
from .types_abstract import cg_typed_value_type
from .types_builtin  import cg_map_case

class cg_processor_cpp(cg_processor):
  def __init__(self, trunk:cg_tree.symbol_node):
    super().__init__(trunk)
      
  @override
  def preprocess_node_specific(self, node:cg_tree.symbol_node):
    if "gaos" in node.tags:
      if node.identifier == "gaos__refl_t":
        return self.preprocess_node_specific_gaos_refl_t(node)
    elif node.symbol_type in [ cg_tree.symbol_node_type.POD, cg_tree.symbol_node_type.ENUM ]:
      return self.preprocess_node_specific_add_gaos_refl_t(node)
    return True, []
  
  def preprocess_node_specific_add_gaos_refl_t(self, node:cg_tree.symbol_node):
    child = node.ensure_child("~refl")
    child.change_to_type_or_fail(cg_tree.symbol_node_type.LINK)
      
    link:cg_typed_value() = cg_typed_value()
    link.type_t    = cg_typed_value_type.AUTO
    link.content_t = cg_typed_value_type.PATH
    link.content   = [ "gaos__refl_t" ]
    child.dangling_objects.append(link)
    
    return True, [ child ]
  
  def preprocess_node_specific_gaos_refl_t(self, node:cg_tree.symbol_node):
    functions = [ "get_tokens" ]
    added     = []    

    for fn in functions:
      child = node.ensure_child(fn)
      added.append(child)
      child.change_to_type_or_fail(cg_tree.symbol_node_type.FN)
      child.tags += [ "gaos__refl_t", "impl_defined" ]

    return True, added

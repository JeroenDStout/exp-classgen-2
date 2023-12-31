import copy
from .               import tree            as cg_tree
from .reader_stack   import cg_reader_stack
from .types_abstract import cg_typed_value
from .types_abstract import cg_typed_value_type
from .types_builtin  import cg_map_case
    
#
#
#
class cg_processor():
  def __init__(self, trunk:cg_tree.symbol_node):
    self.trunk:cg_tree.symbol_node = trunk
    self.dirty_nodes:list[cg_tree.symbol_node]      = None
    self.next_dirty_nodes:list[cg_tree.symbol_node] = []
    self.trunk.add_nodes_to_list_recursively(self.next_dirty_nodes)

  def process(self):
    self.process_links()
    self.process_local_aliases()
    
  #
  #
  #
  def process_links(self):
    dirty_nodes:list[cg_tree.symbol_node] = [ node for node in cg_tree.visit_symbol_nodes(self.trunk) if node.symbol_type == cg_tree.symbol_node_type.LINK ]
    dirty_nodes = self.try_repeat_resolve(dirty_nodes, self.process_links_in_node)
    if len(dirty_nodes):
      print("ERROR: Could not complete process_links")
      
  def process_links_in_node(self, node:cg_tree.symbol_node):
    if node.symbol_type != cg_tree.symbol_node_type.LINK:
      return True, []
    
    links_to_try:list[cg_typed_value] = [ obj for obj in node.dangling_objects if type(obj) == cg_typed_value ]
    new_nodes:list[cg_tree.symbol_node] = []
    
    all_succeeded = True
    for obj in links_to_try:
      if not self.try_resolve_dangling_object(node, obj):
        all_succeeded = False
        continue
      
      new_nodes += self.process_node_link(obj.content, node.parent)
      
    return all_succeeded, new_nodes
      
  def process_node_link(self, src:cg_tree.symbol_node, dest:cg_tree.symbol_node):
    return self.duplicate_children_shallowly(src, dest)
    
  #
  #
  #
  def process_local_aliases(self):
    dirty_nodes:list[cg_tree.symbol_node] = [ node for node in cg_tree.visit_symbol_nodes(self.trunk) if node.symbol_type == cg_tree.symbol_node_type.ALIAS_LOCAL ]
    dirty_nodes = self.try_repeat_resolve(dirty_nodes, self.process_local_alias_of_node)
    if len(dirty_nodes):
      print("ERROR: Could not complete process_local_aliases")
      
  def process_local_alias_of_node(self, node:cg_tree.symbol_node):
    if node.symbol_type != cg_tree.symbol_node_type.ALIAS_LOCAL:
      return True, []
    
    if not node.symbol_target:
      print("no symbol target??")
      return True, []
    
    node.symbol_target.dangling_objects.extend(node.dangling_objects)
    node.dangling_objects = []
    return True, []
  
  #
  #
  #
  def duplicate_children_shallowly(self, source:cg_tree.symbol_node, dest:cg_tree.symbol_node):
    new_nodes = []

    for child in source.children:
      if child.symbol_type in [ cg_tree.symbol_node_type.ALIAS_LOCAL ]:
        continue
      
      sub_node = dest.ensure_child(child.identifier)
      new_nodes.append(sub_node)
      sub_node.tags.append("inherited")
        
      if child.symbol_type not in [ cg_tree.symbol_node_type.FN_MAP ]:
        sub_node.change_to_type_or_fail(cg_tree.symbol_node_type.ALIAS)
        sub_node.symbol_target = child
        continue
          
      sub_node.change_to_type_or_fail(child.symbol_type)
      sub_node.tags += child.tags
      
      for subchild in child.children:
        sub_node = sub_node.ensure_child(subchild.identifier)
        sub_node.change_to_type_or_fail(cg_tree.symbol_node_type.ALIAS)
        sub_node.symbol_target = child
        
    return new_nodes
  
  #
  #
  #
  def try_repeat_resolve(self, dirty_nodes:list[cg_tree.symbol_node], fn_try_resolve):
    iterations:int = 0
    next_dirty_nodes:list[cg_tree.symbol_node] = []
    any_resolved:bool = True
    
    while len(dirty_nodes) and any_resolved:
      any_resolved = False
      next_dirty_nodes = []
      iterations += 1
      
      # debug
      #print("[" + str(iterations) + "]")
      #for node in dirty_nodes:
      #  print("Dirty " + "::".join(node.get_canonical_path()))
      #  print("      " + node.to_big_string().replace("\n", "\n      "))
      #
      #if iterations > 10:
      #  print("ERROR: try_repeat_resolve ran out of iterations")
      #  for node in dirty_nodes:
      #    print("See ::" + "::".join(node.get_canonical_path()))
      #    print("      " + node.to_big_string().replace("\n", "\n      "))
      #  return dirty_nodes
      
      for node in dirty_nodes:
        all_resolved_in_node, new_nodes = fn_try_resolve(node)
        next_dirty_nodes += new_nodes
        
        if not all_resolved_in_node:
          next_dirty_nodes.append(node)
          continue
        
        any_resolved = True
      
      if not any_resolved:
        print("ERROR: try_repeat_resolve could not resolve any node in iteration")
        for node in next_dirty_nodes:
          print("See ::" + "::".join(node.get_canonical_path()))
          print("      " + node.to_big_string().replace("\n", "\n      "))
        return next_dirty_nodes

      dirty_nodes = next_dirty_nodes
      
    return []
  
  #
  #
  #
  def try_resolve_dangling_object(self, parent:cg_tree.symbol_node, dangling_object):
    if type(dangling_object) == cg_typed_value:
      typed_value:cg_typed_value = dangling_object
      
      if typed_value.content_t != cg_typed_value_type.PATH:
        return True
      
      obj = parent.resolve_path(typed_value.content)
      if obj == None:
        return False
      
      typed_value.content_t = cg_typed_value_type.OBJECT
      typed_value.content   = obj
      return True
    
    return True
    

    
        

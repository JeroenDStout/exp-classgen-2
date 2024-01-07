import copy
from os  import path as os_path
from .   import tree as cg_tree

#
#
#
class cg_writer():
  def __init__(self, trunk:cg_tree.symbol_node):
    self.trunk:cg_tree.symbol_node = trunk

  def write_if_updated(self, out_path:str, contents:list[str]):
    if os_path.isfile(out_path):
      with open(out_path, 'r') as old_file:
        if old_file.readlines() == contents:
          return
    with open(out_path, 'w') as new_file:
      new_file.write('\n'.join(contents))
    
        
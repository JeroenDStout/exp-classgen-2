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
    content = '\n'.join(contents)
    
    if os_path.isfile(out_path):
      with open(out_path, 'r') as old_file:
        old_content = old_file.read()
        if old_content == content:
          print(f"* ({os_path.basename(out_path)} was up to date)")
          return          
          
    with open(out_path, 'w') as new_file:
      new_file.write('\n'.join(contents))
      
    print(f"* {os_path.basename(out_path)} updated")
    
        
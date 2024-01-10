from calendar import c
from msilib.schema import File
from overrides import override
from .               import tree            as cg_tree
from .writer         import cg_writer

#
#
#
class cg_writer_cpp(cg_writer):
  def __init__(self, trunk:cg_tree.symbol_node):
    super().__init__(trunk)

  def get_block_gen_warning(self):
    return [
      "//",
      "//   This file was generated by classgen writer_cpp",
      "//            please do not edit by hand",
      "//"
    ]

  def get_block_initial_h(self):
    return [ "#pragma once", "" ] + self.get_block_gen_warning() + [ "" ]

  def get_block_initial_cpp(self):
    return self.get_block_gen_warning() + [ "" ]

  def write_cpp(self, out_path:str, proj_name:str, base_name:str):
    self.proj_name = proj_name
    self.base_name = base_name
    self.write(out_path)
    
  @override
  def write_visit_enter(self, node:cg_tree.symbol_node):
    if node.symbol_type == cg_tree.symbol_node_type.NAMESPACE:
      return [
        self.meta_symbol(self.meta_symbol_type.OPTIONAL_SPACE, 1),
        "namespace " + node.identifier + " {",
        self.meta_symbol(self.meta_symbol_type.INDENT, 4),
      ]
    return []
    
  @override
  def write_visit_leave(self, node:cg_tree.symbol_node):
    if node.symbol_type == cg_tree.symbol_node_type.NAMESPACE:
      return [
        self.meta_symbol(self.meta_symbol_type.INDENT, -4),
        "}",
        self.meta_symbol(self.meta_symbol_type.OPTIONAL_SPACE, 1)
      ]
    return []
    
  def write_enum_block(self, node:cg_tree.symbol_node):
    tokens = node.resolve_path([ "~tokens" ], True, False)
    if tokens:
      ret = []
      for child in tokens.children:
        ret += [
          self.meta_symbol(self.meta_symbol_type.OPTIONAL_COMMA, 1),
          child.identifier,
          self.meta_symbol(self.meta_symbol_type.OPTIONAL_COMMA, 1),
        ]
      return ret

    return []


#
#
#
class cg_writer_cpp_decl_h(cg_writer_cpp):
  def __init__(self, trunk:cg_tree.symbol_node):
    super().__init__(trunk)

  @override
  def write_intro(self):
    return self.get_block_initial_h()

  @override
  def get_visit_type(self, node:cg_tree.symbol_node):
    if node.symbol_type in [
        cg_tree.symbol_node_type.REFL
        ]:
      return self.visit_type.NONE
      
    if node.symbol_type in [
        cg_tree.symbol_node_type.ENUM,
        cg_tree.symbol_node_type.POD
        ]:
      return self.visit_type.WRITE
      
    return self.visit_type.ENTER

  @override
  def write_visit_specific(self, node:cg_tree.symbol_node):
    match node.symbol_type:
      case cg_tree.symbol_node_type.ENUM:
        return [
          self.meta_symbol(self.meta_symbol_type.OPTIONAL_SPACE, 1),
          "enum " + node.identifier + " : unsigned char;",
          self.meta_symbol(self.meta_symbol_type.OPTIONAL_SPACE, 1)
        ]
      case cg_tree.symbol_node_type.POD:
        return [ 
          self.meta_symbol(self.meta_symbol_type.OPTIONAL_SPACE, 1),
          "// pod",
          "struct " + node.identifier + ";",
          self.meta_symbol(self.meta_symbol_type.OPTIONAL_SPACE, 1)
        ]

#
#
#
class cg_writer_cpp_impl_h(cg_writer_cpp):
  def __init__(self, trunk:cg_tree.symbol_node):
    super().__init__(trunk)
    
  @override
  def write_intro(self):
    return (
      self.get_block_initial_h()
    + [ f'#include "{self.proj_name}/{self.base_name}_decl.h"', "" ]
    )

  @override
  def get_visit_type(self, node:cg_tree.symbol_node):
    if node.symbol_type in [
        cg_tree.symbol_node_type.REFL
        ]:
      return self.visit_type.NONE
      
    if node.symbol_type in [
        cg_tree.symbol_node_type.ENUM,
        cg_tree.symbol_node_type.POD,
        cg_tree.symbol_node_type.FN,
        cg_tree.symbol_node_type.FN_MAP
        ]:
      return self.visit_type.WRITE
      
    return self.visit_type.ENTER

  @override
  def write_visit_specific(self, node:cg_tree.symbol_node):
    match node.symbol_type:
      case cg_tree.symbol_node_type.ENUM:
        return [
          self.meta_symbol(self.meta_symbol_type.OPTIONAL_SPACE, 1),
          "enum " + node.identifier + " : unsigned char {",
          self.meta_symbol(self.meta_symbol_type.INDENT, 4),
        ] + self.write_enum_block(node) + [
          self.meta_symbol(self.meta_symbol_type.INDENT, -4),
          "};",
          self.meta_symbol(self.meta_symbol_type.OPTIONAL_SPACE, 1)
        ]
      case cg_tree.symbol_node_type.POD:
        return [ 
          self.meta_symbol(self.meta_symbol_type.OPTIONAL_SPACE, 1),
          "// pod",
          "struct " + node.identifier + " {",
          self.meta_symbol(self.meta_symbol_type.INDENT, 4),
          "// ...",
          self.meta_symbol(self.meta_symbol_type.INDENT, -4),
          "};",
          self.meta_symbol(self.meta_symbol_type.OPTIONAL_SPACE, 1)
        ]
      case cg_tree.symbol_node_type.FN:
        return [ 
          self.meta_symbol(self.meta_symbol_type.OPTIONAL_SPACE, 1),
          "// fn " + node.identifier + ";",
          self.meta_symbol(self.meta_symbol_type.OPTIONAL_SPACE, 1)
        ]
      case cg_tree.symbol_node_type.FN_MAP:
        return [ 
          self.meta_symbol(self.meta_symbol_type.OPTIONAL_SPACE, 1),
          "// fn_map " + node.identifier + ";",
          self.meta_symbol(self.meta_symbol_type.OPTIONAL_SPACE, 1)
        ]

#
#
#
class cg_writer_cpp_cpp(cg_writer_cpp):
  def __init__(self, trunk:cg_tree.symbol_node):
    super().__init__(trunk)
    
  @override
  def write_intro(self):
    return (
      self.get_block_initial_h()
    + [ f'#include "{self.proj_name}/{self.base_name}_decl.h"',
        f'#include "{self.proj_name}/{self.base_name}_impl.h"',"" ]
    )
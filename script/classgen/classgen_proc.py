import sys
import antlr4
import math

#print(sys.argv)

# add our antlr generated files path
sys.path.insert(0, sys.argv[1])

from classgen_grammarLexer   import classgen_grammarLexer
from classgen_grammarParser  import classgen_grammarParser
from classgen_grammarVisitor import classgen_grammarVisitor

from classgen import debug         as cg_debug
from classgen import reader        as cg_reader
from classgen import processor     as cg_processor
from classgen import processor_cpp as cg_processor_cpp
from classgen import writer        as cg_writer
from classgen import writer_cpp    as cg_writer_cpp

sys_arg = {}
for arg in sys.argv[2:]:
  data = arg.split(':', 1)
  if len(data) == 2:
    sys_arg[data[0]] = data[1]
    continue
  print("Badly formatted argument: \"" + arg + "\"")
  
with open(sys_arg["in"]) as file:
  data = file.read()
     
lexer  = classgen_grammarLexer(antlr4.InputStream(data))
stream = antlr4.CommonTokenStream(lexer)
parser = classgen_grammarParser(stream)

# debug
#stream.fill()
#for token in stream.tokens:
#  if token.type < 0:
#    print("<EOF>")
#    break
#  print(str(token.type) + ": " + lexer.symbolicNames[token.type - 1])

tree    = parser.prog()

# debug
#visitor = cg_debug.classgen_debug_visitor(parser)
#visitor.visit(tree)

visitor = cg_reader.cg_reader_visitor(parser)
visitor.visit(tree)
# debug
#print(visitor.trunk.to_big_string())

processor = cg_processor_cpp.cg_processor_cpp(visitor.trunk)
processor.process()
# debug
#print(processor.trunk.to_big_string())

writer = cg_writer_cpp.cg_writer_cpp(processor.trunk)
if "out_decl_h" in sys_arg: writer.write_decl_h(sys_arg["out_decl_h"], sys_arg["proj"], sys_arg["obj"])
if "out_impl_h" in sys_arg: writer.write_impl_h(sys_arg["out_impl_h"], sys_arg["proj"], sys_arg["obj"])
if "out_cpp"    in sys_arg: writer.write_cpp(   sys_arg["out_cpp"   ], sys_arg["proj"], sys_arg["obj"])

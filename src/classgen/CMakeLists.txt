init_directory(classgen)

# Define the Version project
init_project(classgen "support")

# Sources static
setup_project_source(classgen "grammar"
  src:
    classgen_grammar.g4
)
setup_project_source(classgen "core"
  script:
    classgen_proc.py
)
setup_project_source(classgen "core/classgen"
  script:
    classgen/debug.py
    classgen/reader.py
    classgen/reader_stack.py
    classgen/writer.py
    classgen/types.py
    classgen/tree.py
)

# Antlr files
set(antlr_generated_files)
antlr_py_build_single(${abs_can_src}/classgen_grammar.g4 "antlr" antlr_generated_files)
setup_project_source_specific(classgen "lang/generated" "generated;script" ${antlr_generated_files})
 
# Target
configure_project_script(classgen)
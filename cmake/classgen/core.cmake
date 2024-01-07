set(classgen_can_script "${cmake_can_script}/classgen")
set(classgen_gen_script "${cmake_gen_script}/classgen")

function(classgen_proc_single_cxx source
         destination_cpp destination_h
         append_generated_cpp append_generated_h
        )
  # ...
  sources_get_canonprint_filepath(${source} source_relpath)
  sources_get_canonprint_filepath("${abs_gen_src}/${destination_cpp}" destination_cpp_relpath)
  sources_get_canonprint_filepath("${abs_gen_include}/${destination_h}" destination_h_relpath)
  
  # ...
  file(MAKE_DIRECTORY "${abs_gen_src}/${destination_cpp}")
  file(MAKE_DIRECTORY "${abs_gen_include}/${destination_h}")
  get_filename_component(base_out_name ${source} NAME_WLE)
  
  # ...
  set(loc_gen_cpp ${${append_generated_cpp}})
  set(loc_gen_h ${${append_generated_h}})
  list(APPEND loc_gen_cpp "${destination_cpp}/${base_out_name}.cpp")
  list(APPEND loc_gen_h   "${destination_h}/${base_out_name}_decl.h")
  list(APPEND loc_gen_h   "${destination_h}/${base_out_name}_impl.h")
  
  message(STATUS "Classgen setup: ${source_relpath} -> ${destination_relpath}")
  message(STATUS " - ${destination_cpp}/${base_out_name}.cpp")
  message(STATUS " - ${destination_h}/${base_out_name}_decl.h")
  message(STATUS " - ${destination_h}/${base_out_name}_impl.h")
  
  add_custom_command(
    COMMENT           "Classgen: ${source_relpath}"
    OUTPUT            "${abs_gen_src}/${destination_cpp}/${base_out_name}.cpp"
                      "${abs_gen_include}/${destination_h}/${base_out_name}_decl.h"
                      "${abs_gen_include}/${destination_h}/${base_out_name}_impl.h"
    COMMAND           ${Python3_EXECUTABLE}
                      "${classgen_can_script}/classgen_proc.py"
                      "${classgen_gen_script}/antlr"
                      "proj:${proj_dir_name}"
                      "obj:${base_out_name}"
                      "in:${source}"
                      "out_cpp:${abs_gen_src}/${destination_cpp}/${base_out_name}.cpp"
                      "out_decl_h:${abs_gen_include}/${destination_h}/${base_out_name}_decl.h"
                      "out_impl_h:${abs_gen_include}/${destination_h}/${base_out_name}_impl.h"
    DEPENDS           ${classgen_can_script}/classgen_proc.py
                      ${source}
    VERBATIM
  )
  
  set(${append_generated_cpp} ${loc_gen_cpp} PARENT_SCOPE)
  set(${append_generated_h}   ${loc_gen_h}   PARENT_SCOPE)
endfunction()

function(configure_project_classgen proj)
  message(STATUS "Set up dependency on classgen")
  add_dependencies(${proj} classgen)
endfunction()
set(classgen_can_script "${cmake_can_script}/classgen")
set(classgen_gen_script "${cmake_gen_script}/classgen")

function(classgen_proc_single source destination append_generated)
  sources_get_canonprint_filepath(${source} source_relpath)
  sources_get_canonprint_filepath("${abs_gen_include}/${destination}" destination_relpath)
  
  get_filename_component(base_out_name ${source} NAME_WLE)
  
  set(loc_gen ${${append_generated}})
  list(APPEND loc_gen "${destination}/${base_out_name}.h")
  # 
  message(STATUS "Classgen setup: ${source_relpath} -> ${destination_relpath}")
  message(STATUS " - ${destination}/${base_out_name}.h")
  
  file(MAKE_DIRECTORY "${abs_gen_include}/${destination}")
  
  add_custom_command(
    COMMENT           "Classgen: ${source} -> ${abs_gen_include}/${destination}/${base_out_name}.h"
    OUTPUT            "${abs_gen_include}/${destination}/${base_out_name}.h"
    COMMAND           ${Python3_EXECUTABLE}
                      "${classgen_can_script}/classgen_proc.py"
                      "${classgen_gen_script}/antlr"
                      "in:${source}"
                      "out_h:${abs_gen_include}/${destination}/${base_out_name}.h"
    DEPENDS           ${classgen_script_dir}/classgen_proc.py
                      ${source}
    WORKING_DIRECTORY "${abs_gen_include}/${destination}/"
    VERBATIM
  )
  
  set(${append_generated} ${loc_gen} PARENT_SCOPE)
endfunction()

function(configure_project_classgen proj)
  message(STATUS "Set up dependency on classgen")
  add_dependencies(${proj} classgen)
endfunction()
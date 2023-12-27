init_directory(experiment)

include(${CMAKE_SOURCE_DIR}/cmake/classgen/core.cmake)

# Define the Experiment project
init_project(experiment "core")

# Sources static
setup_project_source(experiment "core"
  src:
    experiment.cpp
  include:
    experiment.h
)
setup_project_source(experiment "data"
  src:
    data_enum_test.clgen
)

# Classgen
set(classgen_generated_inc)
classgen_proc_single(${abs_can_src}/data_enum_test.clgen "" classgen_generated_inc)
setup_project_source_specific(experiment "data/generated" "generated;include" ${classgen_generated_inc})

# Target
configure_project_executable(experiment)
configure_cxx_target(experiment)
configure_publish_exec(experiment)
configure_project_classgen(experiment)

add_dependencies(experiment version classgen)

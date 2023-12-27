init_directory(experiment)

# Define the Experiment project
init_project(experiment "core")

# Sources static
setup_project_source(experiment "core"
  src:
    experiment.cpp
  include:
    experiment.h
)

# Target
configure_project_executable(experiment)
configure_cxx_target(experiment)
configure_publish_exec(experiment)

add_dependencies(experiment version)
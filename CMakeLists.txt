#
# Initial set-up
#

cmake_minimum_required(VERSION 3.15)

project(classgen)
include(cmake/generic/project.cmake)
include(cmake/generic/publish.cmake)

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

# Languages
include(cmake/generic/cxx.cmake)
include(cmake/generic/python.cmake)

# Support
include(cmake/generic/artefacts.cmake)
include(cmake/generic/sources.cmake)

# Processing
include(cmake/generic/antlr.cmake)

# Subprojects
add_subdirectory(src/experiment)
add_subdirectory(src/version)

# Publication
finalise_publish()
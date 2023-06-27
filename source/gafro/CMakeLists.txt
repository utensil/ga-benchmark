set(gafro_SUCCESS true)

# Find gafro library
find_library(gafro_LIBRARY NAMES gafro HINTS "${CMAKE_CURRENT_SOURCE_DIR}/libs/gafro/install/usr/local/lib/gafro")
if(NOT EXISTS ${gafro_LIBRARY})
  # message(WARNING "The path defined in gafro_LIBRARY doesn't exist.")
  set(gafro_SUCCESS false)
endif()

find_package(Eigen3)
# # Set (global) properties
# set(gafro_PROPERTIES
#   PROPERTY VALUE
# )

# Set (global) include directories and libraries
set(gafro_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/libs/gafro/install/usr/local/include/gafro" CACHE PATH "The include directory of the gafro library.")
set(gafro_INCLUDE_EXTRA_DIR "${EIGEN3_INCLUDE_DIR}") # no dependencies

if(NOT EXISTS ${gafro_INCLUDE_DIR})
  # message(WARNING "The path defined in gafro_INCLUDE_DIR doesn't exist.")
  set(gafro_SUCCESS false)
endif()

set(gafro_LIBS_INIT ${gafro_LIBRARY})

# Set include directories and libraries for inverse kinematics
set(gafro_AlgorithmInverseKinematics_INCLUDE_DIR "")
set(gafro_AlgorithmInverseKinematics_LIBS_INIT "")

# Set include directories and libraries for binary operations
set(gafro_BinaryOperations_INCLUDE_DIR "")
set(gafro_BinaryOperations_LIBS_INIT "")

# Set include directories and libraries for unary operations
set(gafro_UnaryOperations_INCLUDE_DIR "")
set(gafro_UnaryOperations_LIBS_INIT "")

# Job done!
if(${gafro_SUCCESS})
  set(gafro_ENABLED true CACHE BOOL "If set, the gafro library will be added to the benchmark.")
else()
  set(gafro_ENABLED false CACHE BOOL "If set, the gafro library will be added to the benchmark." FORCE)
endif()
set(GAL_SUCCESS true)
# set(GAL_ENABLED true)
# Set (global) include directories and libraries
set(GAL_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/libs/GAL/public" CACHE PATH "The include directory of the GAL library.")
set(GAL_INCLUDE_EXTRA_DIR "") # no dependencies

if(NOT EXISTS ${GAL_INCLUDE_DIR})
  message(WARNING "The path defined in GAL_INCLUDE_DIR doesn't exist.")
  set(GAL_SUCCESS false)
else()
  message(STATUS "The path defined in GAL_INCLUDE_DIR exists.")
endif()

set(GAL_LIBS_INIT ${GAL_LIBRARY})

# Set include directories and libraries for inverse kinematics
set(GAL_AlgorithmInverseKinematics_INCLUDE_DIR "")
set(GAL_AlgorithmInverseKinematics_LIBS_INIT "")

# Set include directories and libraries for binary operations
set(GAL_BinaryOperations_INCLUDE_DIR "")
set(GAL_BinaryOperations_LIBS_INIT "")

# Set include directories and libraries for unary operations
set(GAL_UnaryOperations_INCLUDE_DIR "")
set(GAL_UnaryOperations_LIBS_INIT "")

# Job done!
if(${GAL_SUCCESS})
  message(STATUS "Enabling GAL library.")
  set(GAL_ENABLED true)
else()
  message(STATUS "Disabling GAL library.")
  set(GAL_ENABLED false)
endif()


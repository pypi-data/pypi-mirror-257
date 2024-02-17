#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "vecs2pauli::vecs2pauli" for configuration "Release"
set_property(TARGET vecs2pauli::vecs2pauli APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(vecs2pauli::vecs2pauli PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/vecs2pauli.lib"
  )

list(APPEND _cmake_import_check_targets vecs2pauli::vecs2pauli )
list(APPEND _cmake_import_check_files_for_vecs2pauli::vecs2pauli "${_IMPORT_PREFIX}/lib/vecs2pauli.lib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

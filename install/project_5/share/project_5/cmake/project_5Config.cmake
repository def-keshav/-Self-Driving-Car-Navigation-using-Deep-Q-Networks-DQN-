# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_project_5_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED project_5_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(project_5_FOUND FALSE)
  elseif(NOT project_5_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(project_5_FOUND FALSE)
  endif()
  return()
endif()
set(_project_5_CONFIG_INCLUDED TRUE)

# output package information
if(NOT project_5_FIND_QUIETLY)
  message(STATUS "Found project_5: 0.0.0 (${project_5_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'project_5' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${project_5_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(project_5_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${project_5_DIR}/${_extra}")
endforeach()

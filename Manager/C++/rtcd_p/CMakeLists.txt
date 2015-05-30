cmake_minimum_required (VERSION 2.6)

find_package(OpenRTM REQUIRED)


include_directories(${OPENRTM_INCLUDE_DIRS})
include_directories(${OMNIORB_INCLUDE_DIRS})
add_definitions(${OPENRTM_CFLAGS})
add_definitions(${OMNIORB_CFLAGS})


link_directories(${OPENRTM_LIBRARY_DIRS})
link_directories(${OMNIORB_LIBRARY_DIRS})


project (rtcd_p)

add_executable (rtcd_p rtcd_p.cpp)
target_link_libraries(rtcd_p ${OPENRTM_LIBRARIES})
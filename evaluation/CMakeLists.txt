find_package(scatter REQUIRED)
find_package(yaml-cpp REQUIRED)

add_executable(plot_results main.cpp)
target_include_directories(plot_results PUBLIC ${YAML_CPP_INCLUDE_DIRS})
target_link_libraries(plot_results PUBLIC scatter::scatter ${YAML_CPP_LIBRARIES})
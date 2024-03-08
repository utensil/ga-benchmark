#include <filesystem>
#include <iostream>
//
#include <yaml-cpp/yaml.h>

#include <scatter/scatter.hpp>

int main(int /*argc*/, char ** /*argv*/)
{
    std::vector<std::string> libraries = {
        "gafro",   //
        "GATL",    //
                   // "Garamon",  //
                   // "TbGAL",    //
        "Gaalet",  //
        "Versor"   //
    };

    std::map<std::string, scatter::Colour> colors = {
        { "GATL", scatter::Colour(253, 127, 111, 255) },  //
        // { "Garamon", scatter::Colour(178, 224, 97, 255) },  //
        // { "TbGAL", scatter::Colour(255, 238, 101, 255) },   //
        { "Gaalet", scatter::Colour(189, 126, 190, 255) },  //
        { "Versor", scatter::Colour(255, 181, 90, 255) },   //
        { "gafro", scatter::Colour(126, 176, 213, 255) },   //
        // "#beb9db",
        // "#fdcce5",
        // "#8bd3c7";
    };

    std::map<std::string, std::string> titles = {
        { "Addition", "Addition" },                   // ev
        { "GeometricProduct", "Geometric Product" },  //"#7eb0d5" },  //
        { "HestenesInnerProduct", "Inner Product" },  //"#b2e061" },    //
        { "OuterProduct", "Outer Product" },          //"#bd7ebe" },   //
    };

    std::vector<std::string> unary_operations = { "Dualization", "Reversion", "Inversion" };
    std::vector<std::string> binary_operations = { "Addition", "HestenesInnerProduct", "OuterProduct", "GeometricProduct" };

    {
        scatter::FigureOptions figure_options;
        figure_options.setHeight(1000.0);
        figure_options.setWidth(3300.0);

        scatter::Figure figure(figure_options, 1, 3);

        int col = 0;

        // PARSE UNARY OPERATIONS
        for (const std::string &operation : unary_operations)
        {
            std::cout << operation << std::endl;

            scatter::Plot::Ptr plot = scatter::Plot::create(operation);
            plot->options().getTitleOptions().setSize(50);

            double max = 0.0;

            for (const std::string &library : libraries)
            {
                std::vector<scatter::Point> values;

                for (unsigned grade = 0; grade < 6; ++grade)
                {
                    std::string filename = "GABenchmark_UnaryOperations_ConformalModel_D3_GRADE" + std::to_string(grade) + "_" + library + ".json";

                    YAML::Node yaml = YAML::LoadFile(filename);

                    for (const auto &node : yaml["benchmarks"])
                    {
                        if (node["error_message"])
                        {
                            continue;
                        }

                        if (node["name"].as<std::string>().find(operation) != std::string::npos)
                        {
                            if (node["aggregate_name"].as<std::string>() == "mean")
                            {
                                double value = node["real_time"].as<double>();

                                values.push_back(scatter::Point(double(grade), value));

                                max = std::max(max, value);
                            }
                        }
                    }
                }

                scatter::LinePlot::Options options;
                // options.setLabel(library);
                options.setThickness(5.0);
                // options.setColour(colors[library]);

                plot->add<scatter::LinePlot>(library, values, options);
            }

            plot->options().getTextOptions().setSize(40);
            plot->options().getAxisOptions().setYPrecision(4);
            plot->options().getAxisOptions().setYmax(std::ceil(max / 10.0) * 10.0);
            plot->options().getAxisOptions().setXmax(5.0);
            plot->options().getAxisOptions().setShowGrid(true);
            plot->options().getAxisOptions().setYticks(10.0);
            plot->options().getAxisOptions().setXticks(5.0);
            plot->options().getAxisOptions().setXlabel("");
            plot->options().getAxisOptions().setYlabel("");
            plot->options().getLegendOptions().setAnchor(scatter::Anchor::NORTH_WEST);

            if (col > 0)
            {
                plot->options().getLegendOptions().setShow(false);
            }
            if (col == 0)
            {
                plot->options().getAxisOptions().setYlabel("Time [ns]");
            }
            // if (col == 1)
            // {
            // }
            plot->options().getAxisOptions().setXlabel("Grade");

            // plot->save("Benchmark_" + operation + ".pdf");
            figure.add(plot, 0, col++);
        }

        figure.save("BenchmarkUnaryOperations.pdf");
    }

    // PARSE BINARY OPERATIONS
    {
        scatter::FigureOptions figure_options;
        figure_options.setHeight(1000.0);
        figure_options.setWidth(4400.0);

        scatter::Figure figure(figure_options, 1, 4);

        int col = 0;

        for (const std::string &operation : binary_operations)
        {
            std::cout << operation << std::endl;

            scatter::Plot::Ptr plot = scatter::Plot::create(titles[operation]);
            plot->options().getTitleOptions().setSize(50);

            double max = 0.0;

            for (const std::string &library : libraries)
            {
                std::vector<scatter::Point> values;

                for (unsigned left_grade = 0; left_grade < 6; ++left_grade)
                {
                    for (unsigned right_grade = 0; right_grade < 6; ++right_grade)
                    {
                        std::string filename = "GABenchmark_BinaryOperations_ConformalModel_D3_LEFTGRADE" + std::to_string(left_grade) +
                                               "_RIGHTGRADE" + std::to_string(right_grade) + "_" + library + ".json";

                        YAML::Node yaml;

                        try
                        {
                            yaml = YAML::LoadFile(filename);
                        }
                        catch (...)
                        {
                            continue;
                        }

                        for (const auto &node : yaml["benchmarks"])
                        {
                            if (node["error_message"])
                            {
                                continue;
                            }

                            if (node["name"].as<std::string>().find(operation) != std::string::npos)
                            {
                                if (node["aggregate_name"].as<std::string>() == "mean")
                                {
                                    double value = node["real_time"].as<double>();

                                    values.push_back(scatter::Point(double(left_grade * 6 + right_grade), value));

                                    max = std::max(max, value);
                                }
                            }
                        }
                    }
                }

                scatter::LinePlot::Options options;
                // options.setLabel(library);
                options.setThickness(5.0);
                // options.setColour(colors[library]);

                plot->add<scatter::LinePlot>(library, values, options);
            }

            plot->options().getTextOptions().setSize(40);
            plot->options().getAxisOptions().setYPrecision(4);
            plot->options().getAxisOptions().setYmax(std::ceil(max / 10.0) * 10.0);
            plot->options().getAxisOptions().setXmax(36.0);
            plot->options().getAxisOptions().setShowGrid(true);
            plot->options().getAxisOptions().setYticks(10.0);
            plot->options().getAxisOptions().setXticks(6.0);
            plot->options().getAxisOptions().setXlabel("");
            plot->options().getAxisOptions().setYlabel("");
            plot->options().getLegendOptions().setAnchor(scatter::Anchor::NORTH_WEST);

            if (col > 0)
            {
                plot->options().getLegendOptions().setShow(false);
            }
            if (col == 0)
            {
                plot->options().getAxisOptions().setYlabel("Time [ns]");
            }
            // if (col == 1)
            // {
            // }
            plot->options().getAxisOptions().setXlabel("");

            // plot->save("Benchmark_" + operation + ".pdf");
            figure.add(plot, 0, col++);
        }

        figure.save("BenchmarkBinaryOperations.pdf");
    }

    return 0;
}
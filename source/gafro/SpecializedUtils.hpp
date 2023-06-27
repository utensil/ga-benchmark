/* Copyright(C) ga-developers
 *
 * Repository: https://github.com/ga-developers/ga-benchmark.git
 *
 * This file is part of the GA-Benchmark project.
 *
 * GA-Benchmark is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * GA-Benchmark is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with GA-Benchmark. If not, see <https://www.gnu.org/licenses/>.
 */

#ifndef __GABM_SPECIALIZED_UTILS_HPP__
#define __GABM_SPECIALIZED_UTILS_HPP__

#include <gafro/gafro.hpp>

template <int grade>
auto makeGrade();

template <>
auto makeGrade<0>()
{
    return gafro::Multivector<double, gafro::blades::scalar>(Eigen::Vector<double, 1>::Random());
}

template <>
auto makeGrade<1>()
{
    return gafro::Multivector<double, gafro::blades::e1, gafro::blades::e2, gafro::blades::e3, gafro::blades::ei, gafro::blades::e0>(
      Eigen::Vector<double, 5>::Random());
}

template <>
auto makeGrade<2>()
{
    return gafro::Multivector<double, gafro::blades::e23, gafro::blades::e13, gafro::blades::e12, gafro::blades::e1i, gafro::blades::e2i,
                              gafro::blades::e3i, gafro::blades::e01, gafro::blades::e02, gafro::blades::e03, gafro::blades::e0i>(

      Eigen::Vector<double, 10>::Random());
}

template <>
auto makeGrade<3>()
{
    return gafro::Multivector<double, gafro::blades::e123, gafro::blades::e12i, gafro::blades::e13i, gafro::blades::e23i, gafro::blades::e012,
                              gafro::blades::e013, gafro::blades::e023, gafro::blades::e01i, gafro::blades::e02i, gafro::blades::e03i>(
      Eigen::Vector<double, 10>::Random());
}

template <>
auto makeGrade<4>()
{
    return gafro::Multivector<double, gafro::blades::e123i, gafro::blades::e0123, gafro::blades::e012i, gafro::blades::e023i, gafro::blades::e013i>(

      Eigen::Vector<double, 5>::Random());
}

template <>
auto makeGrade<5>()
{
    return gafro::Multivector<double, gafro::blades::e0123i>(

      Eigen::Vector<double, 1>::Random());
}

GABM_DEFINE_MAKE_BLADE(scalar_factor, vector_factors, grade)
{
    return makeGrade<1>();
}

GABM_DEFINE_SQUARED_REVERSE_NORM(arg, grade)
{
    return arg.squaredNorm();
}

#endif  // __GABM_SPECIALIZED_UTILS_HPP__

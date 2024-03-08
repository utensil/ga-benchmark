import argparse, functools, os, json, shutil, sys
from typing import Tuple

_COMPILER_ID_TO_NAME = {  # Source: https://cmake.org/cmake/help/v3.16/variable/CMAKE_LANG_COMPILER_ID.html
    'Absoft': 'Absoft Fortran',
    'ADSP': 'Analog VisualDSP++',
    'AppleClang': 'Apple Clang',
    'ARMCC': 'ARM Compiler',
    'ARMClang': 'ARM Compiler based on Clang',
    'Bruce': 'Bruce C Compiler',
    'CCur': 'Concurrent Fortran',
    'Clang': 'LLVM Clang',
    'Cray': 'Cray Compiler',
    'Embarcadero': 'Embarcadero',
    'Borland': 'Embarcadero',
    'Flang': 'Flang LLVM Fortran Compiler',
    'G95': 'G95 Fortran',
    'GNU': 'GNU Compiler Collection',
    'GHS': 'Green Hills Software',
    'HP': 'Hewlett-Packard Compiler',
    'IAR': 'IAR Systems',
    'Intel': 'Intel Compiler',
    'MSVC': 'Microsoft Visual Studio',
    'NVIDIA': 'NVIDIA CUDA Compiler',
    'OpenWatcom': 'Open Watcom',
    'PGI': 'The Portland Group',
    'PathScale': 'PathScale',
    'SDCC': 'Small Device C Compiler',
    'SunPro': 'Oracle Solaris Studio',
    'TI': 'Texas Instruments',
    'TinyCC': 'Tiny C Compiler',
    'XL': 'IBM XL',
    'VisualAge': 'IBM XL',
    'zOS': 'IBM XL',
    'XLClang': 'IBM Clang-based XL',
}

MESSAGES = {
    'MISSING_DATA': {
        'description': 'Missing Data',
        'short_description': 'Missing Data',
        'priority': 24.0 * 60 * 60 * 1000  # Milisseconds in one day (much more than the TIMEOUT value in CMake)
    },
    'IMPLEMENTED': {
        'description': 'Implemented',
        'short_description': 'Implemented',
        'priority': 0.0
    },
    'OPERATION_NOT_IMPLEMENTED': {
        'description': 'Operation not Implemented',
        'short_description': 'Operation not Implemented',
        'priority': -1.0
    },
    'MODEL_NOT_IMPLEMENTED': {
        'description': 'Model not Implemented',
        'short_description': 'Model not Implemented',
        'priority': -2.0
    },
    'OPERATION_LEADS_TO_COMPILATION_ERROR': {
        'description': 'Operation Leads to Compilation Error',
        'short_description': 'Compilation Error',
        'priority': -3.0
    },
    'OPERATION_LEADS_TO_RUNTIME_ERROR': {
        'description': 'Operation Leads to Runtime Error',
        'short_description': 'Runtime Error',
        'priority': -4.0
    }
}

_MESSAGE_PRIORITY_TO_KEY = {message_data['priority']: message_key for message_key, message_data in MESSAGES.items()}

METRICS = {
    'cpu_time': {'description': 'CPU time'},
    'real_time': {'description': 'Wall-clock time'}
}

MODELS = {
    'ConformalModel': {
        'description': 'Conformal',
        'id': 0x01
    },
    'EuclideanModel': {
        'description': 'Euclidean',
        'id': 0x02
    },
    'HomogeneousModel': {
        'description': 'Homogeneous',
        'id': 0x03
    },
    'MinkowskiModel': {
        'description': 'Minkowski',
        'id': 0x04
    }
}

_MODEL_ID_TO_KEY = {model_data['id']: model_key for model_key, model_data in MODELS.items()}

OPERATIONS = {
    'Algorithms': {
        'description': 'Algorithms',
        'arguments': {
        },
        'subgroups': {
            'Miscellaneous': {
                'description': 'Miscellaneous',
                'operations': {
                    'InverseKinematics': {'description': 'Inverse Kinematics'}
                }
            }
        }
    },
    'BinaryOperations': {
        'description': 'Binary Operations',
        'arguments': {
            'LeftGrade': {'description': 'LHS Grade'},
            'RightGrade': {'description': 'RHS Grade'}
        },
        'subgroups': {
            'GeometricProducts': {
                'description': 'Main Products',
                'operations': {
                    'CommutatorProduct': {'description': 'Commutator Product'},
                    'GeometricProduct': {'description': 'Geometric Product'},
                    'InverseGeometricProduct': {'description': 'Inverse Geometric Product'}
                }
            },
            'InnerProducts': {
                'description': 'Inner Products',
                'operations': {
                    'DotProduct': {'description': 'Dot Product'},
                    'HestenesInnerProduct': {'description': 'Hestenes\' Inner Product'},
                    'LeftContraction': {'description': 'Left Contraction'},
                    'RightContraction': {'description': 'Right Contraction'},
                    'ScalarProduct': {'description': 'Scalar Product'}
                }
            },
            'NonMetricProducts': {
                'description': 'Non-Metric Products',
                'operations': {
                    'OuterProduct': {'description': 'Outer Product'},
                    'RegressiveProduct': {'description': 'Regressive Product'},
                }
            },
            'SumOperations': {
                'description': 'Sum Operations',
                'operations': {
                    'Addition': {'description': 'Addition'},
                    'Subtraction': {'description': 'Subtraction'}
                }
            }
        }
    },
    'UnaryOperations': {
        'description': 'Unary Operations',
        'arguments': {
            'Grade': {'description': 'Grade'}
        },
        'subgroups': {
            'SignChangeOperations': {
                'description': 'Sign-Change Operations',
                'operations': {
                    'CliffordConjugation': {'description': 'Clifford Conjugation'},
                    'GradeInvolution': {'description': 'Grade Involution'},
                    'Reversion': {'description': 'Reversion'}
                }
            },
            'DualizationOperations': {
                'description': 'Dualization Operations',
                'operations': {
                    'Dualization': {'description': 'Dualization'},
                    'Undualization': {'description': 'Undualization'}
                }
            },
            'NormBasedOperations': {
                'description': 'Norm-Based Operation',
                'operations': {
                    'Inversion': {'description': 'Inversion'},
                    'Normalization': {'description': 'Normalization Under Reverse Norm'},
                    'SquaredReverseNorm': {'description': 'Squared Reverse Norm'},
                }
            },
            'PlusMinusOperations': {
                'description': 'Plus/Minus Operations',
                'operations': {
                    'UnaryMinus': {'description': 'Unary Minus'},
                    'UnaryPlus': {'description': 'Unary Plus'}
                }
            }
        }
    }
}

_OPERATION_KEY_TO_HIERARCHY = {operation_key: (group_key, subgroup_key) for group_key, group_data in OPERATIONS.items() for subgroup_key, subgroup_data in group_data['subgroups'].items() for operation_key in subgroup_data['operations'].keys()}

STATISTICS = {
    'mean': {'description': 'Mean'},
    'median': {'description': 'Median'},
    'stddev': {'description': 'Standard Deviation'}
}

USED_METRIC = 'cpu_time'  # The time that the process actually had the CPU.
# USED_METRIC = 'real_time'  # The wall-clock time, or the actual time taken from the start of the process to the end.


def _context_to_context_key(context: dict) -> Tuple[str, ...]:
    """Convert the context structure into a key for grouping benchmarks evaluated under the same conditions.
    :param context: the context of the benchmark.
    :return: a tuple describing the context.
    """
    return tuple(value for _, value in sorted(context.items()))


def _context_key_to_folder(context_key: Tuple[str, ...]) -> str:
    """Convert the context key into a string.
    :param context_key: the context key of the benchmark.
    :return: a string describing the context.
    """
    return str(context_key[0]) + ''.join(', %s' % str(item) for item in context_key[1:])

def _raw_context_to_partial_context(raw_context: dict) -> dict:
    """Convert the raw context structure into a context structure that includes only the useful field.
    :param raw_context: the context of the benchmark.
    :return: a dictionaty describing the context.
    """
    return {'BuildType': raw_context['library_build_type'], 'NumCPUs': raw_context['num_cpus'], 'MHzPerCPU': raw_context['mhz_per_cpu'], 'CPUScaling': str(raw_context['cpu_scaling_enabled']), 'LoadAvg': str(raw_context['load_avg'][0]) + ''.join(', %s' % str(value) for value in raw_context['load_avg'][1:]), 'Metric': METRICS[USED_METRIC]['description']}

def read_data(folder: str, verbose: bool = False) -> dict:
    """Read benchmark results from JSON files found in the given folder and returns tabulated data.
    :param folder: the path to the folder containing the JSON files generated by the ga-benchmark tool.
    :param verbose: indicates whether the processing messages should be displayed (default: False).
    :return: a dictionary tree with data available in the JSON files and oriented by context/model/d/group/subgroup/operation/solution/case/statistics.
    """
    def message(msg, *argv):
        if verbose: print(msg % argv, end='')
    data = dict()
    success, fail = 0, 0
    message('Reading JSON files in "%s"\n', folder)
    for filename in sorted(os.listdir(folder)) if verbose else tqdm(sorted(os.listdir(folder)), desc='Reading JSON files'):
        filepath = os.path.join(folder, filename)
        if os.path.isfile(filepath) and filename.startswith('GABenchmark_') and filename.endswith('.json'):
            message('  Parsing "%s"... ', filename)
            with open(filepath) as f:
                try:
                    raw_data = json.load(f)
                except:
                    fail += 1  # Errors while trying to load JSON data are the only accepted ones.
                    message('error\n')
                    continue
            partial_context = _raw_context_to_partial_context(raw_data.get('context'))
            for bm in raw_data.get('benchmarks', list()):
                solution_key, operation_key, model_key, d, args, extra_context = _parse_benchmark_name(bm['name'])
                group_key, subgroup_key = _OPERATION_KEY_TO_HIERARCHY[operation_key]
                case_key = tuple(args[argument_key] for argument_key in sorted(OPERATIONS[group_key]['arguments'].keys()))
                if bm.get('error_occurred', False):
                    error_message = bm['error_message']
                    statistics_key = None
                    time = None
                    for message_key, message_data in MESSAGES.items():
                        if error_message.startswith(message_key):
                            time = message_data['priority']
                            break
                    if time is None:
                        raise NotImplementedError('The error message "%s" is not supported yet.' % error_message)
                else:
                    statistics_key = bm.get('aggregate_name', None)
                    time = bm[USED_METRIC]
                context = dict(partial_context, **extra_context)
                context_key = _context_to_context_key(context)
                _, models = data.setdefault(context_key, (context, dict()))
                dimensions = models.setdefault(model_key, dict())
                groups = dimensions.setdefault(d, dict())
                subgroups = groups.setdefault(group_key, dict())
                operations = subgroups.setdefault(subgroup_key, dict())
                solutions = operations.setdefault(operation_key, dict())
                cases = solutions.setdefault(solution_key, dict())
                statistics = cases.setdefault(case_key, dict())
                if statistics_key is not None:
                    statistics[statistics_key] = time
                else:
                    for statistics_key in STATISTICS.keys():
                        statistics[statistics_key] = time
            success += 1
            message('done\n')
    message('  Success: %d, Fail: %d\n\n', success, fail)
    return data

def _parse_benchmark_name(name: str) -> Tuple[str, str, str, str, int, dict, dict]:
    """Parse benchmark name to a set of values.
    :param name: the name of the benchmark.
    :return: (solution_key, operation_key, model_key, d, args, extra_context), where 'solution_key' identifies the library, library generator, or code optimizer, 'operation_key' defines the procedure, 'model_key' and 'd' specify an algebra of R^d, 'args' defines the specialization of the procedure to some case, and 'extra_context' defines some useful information about the context.
    """
    params = name.split('/')
    _, _, operation_key = params[0].split('_')
    solution_key, model_key, d, args, extra_context = None, None, None, dict(), dict()
    for pair in params[1:]:
        key, value = pair.split(':')
        key = key.replace(' ', '');
        if key == 'SystemName' or key == 'SystemVersion' or key == 'CompilerVersion':
            extra_context[key] = value.replace(' ', '')
        elif key == 'CompilerID':
            extra_context['CompilerName'] = value
        elif key == 'Solution':
            solution_key = value.replace(' ', '')
        elif key == 'Model':
            model_key = _MODEL_ID_TO_KEY[int(value, base=16)]
        elif key == 'D':
            d = int(value)
        else:
            try: args[key] = int(value)
            except ValueError: args[key] = value
    return solution_key, operation_key, model_key, d, args, extra_context

def main(argsv=None):
    """Main function.
    """
    if argsv is None: argsv = sys.argv[1:]

    ap = argparse.ArgumentParser('python3 -m plot [-i INPUT_FOLDER] [-o OUTPUT_FOLDER] [-s]')
    ap.add_argument('-i', '--input', metavar='INPUT_FOLDER', required=False, default='.', help='Folder containing the JSON files generated by the ga-benchmark tool (default: current folder).')
    ap.add_argument('-o', '--output', metavar='OUTPUT_FOLDER', required=False, default='./results', help='Folder to which the charts and tables will be exported (default: [current folder]/results).')
    ap.add_argument('-s', '--silent', required=False, default=False, action='store_true', help='Defines whether the processing messages should be skipped. (default: False).')

    args = vars(ap.parse_args(argsv))

    SOLUTIONS = {  # You have to include your solution here if you have added it to ga-benchmark.
        'Gaalet': {'description': 'Gaalet'},
        # 'Gaalop': {'description': 'Gaalop'},
        'Garamon': {'description': 'Garamon'},
        'GATL': {'description': 'GATL'},
        # 'GluCatFramedMulti': {'description': 'GluCat (framed)'},
        # 'GluCatMatrixMulti': {'description': 'GluCat (matrix)'},
        'TbGAL': {'description': 'TbGAL'},
        'Versor': {'description': 'Versor'},
        'gafro': {'description': 'gafro'}
    }

    input_folder = args['input']
    output_folder = args['output']

    data = read_data(folder=input_folder, verbose=not args['silent'])

    print(data)

    json_string = json.dumps(data)
    with open(output_folder+'json_data.json', 'w') as outfile:
        outfile.write(json_string)

if __name__ == "__main__":
    main()
import sys
import re
import random
import shutil

import parser
import distribution

def solve(input_string, report_cumulative=False, analytic=False):
    result_distribution = distribution.DiscreteDistribution({1:1})
    if analytic:
        result_distribution = parser.calculate(input_string, analytic)
        print_graph(result_distribution, report_cumulative)
    else:
        count = 0
        results = {}
        try:
            while True:
                result_sample = parser.calculate(input_string, analytic)
                count += 1

                try:
                    results[result_sample] += 1
                except KeyError:
                    results[result_sample] = 1

                if (count+1)%1000 == 0:
                    result_distribution = distribution.DiscreteDistribution(results)
                    print_height = print_graph(result_distribution, report_cumulative)
                    print(f"\033[F"*(print_height+2))

        except KeyboardInterrupt:
            print_graph(result_distribution, report_cumulative)

def print_graph(results, cumulative=False):
    print("Expected value: {:6.3f}".format(sum(i*results[i]/sum(results.chances()) for i in results.values())))

    if cumulative:
        results = results.get_cumulative()
        count = max(results.chances())
    else:
        count = sum(results.chances())

    maxvalue = max(results.chances())
    maxvalue_len = max(len(str(i)) for i in results.values())
    total_bar_length = shutil.get_terminal_size((80,20))[0]-maxvalue_len-12

    for key in sorted(results.values()):
        bar_length = round(results[key]/maxvalue*total_bar_length)
        print(("{:<"+ str(maxvalue_len+1)+"}{:7.3f}%  {}").format(
                        str(key)+":",
                        results[key]/count*100,
                        u"\u2588"*bar_length + " "*(total_bar_length-bar_length+1)
                      ))
    return len(results.values())

def main(arg_string):
    try:
        instructions, calculation = arg_string.split(':')
    except ValueError:
        instructions, calculation = "", arg_string

    analytic = "A" in instructions
    cumulative = "C" in instructions

    solve(calculation, report_cumulative=cumulative, analytic=analytic)

if __name__ == "__main__":
    main(" ".join(sys.argv[1:]))

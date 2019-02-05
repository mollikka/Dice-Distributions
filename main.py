import sys
import re
import random
import shutil
import math

import parser
import distribution

def solve(input_string, report_cumulative=False, analytic=False, show_odds=False):
    result_distribution = distribution.DiscreteDistribution({1:1})
    if analytic:
        result_distribution = parser.calculate(input_string, analytic)
        print_graph(result_distribution, report_cumulative, show_odds)
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
                    print_height = print_graph(result_distribution, report_cumulative, show_odds)
                    print(f"\033[F"*(print_height+2))

        except KeyboardInterrupt:
            print_graph(result_distribution, report_cumulative, show_odds)

def print_graph(results, cumulative=False, show_odds=False):
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
        if show_odds:
            p_gcd = math.gcd(results[key],count-results[key])
            probs_str = "{}:{}".format(results[key]//p_gcd,(count-results[key])//p_gcd)
            print(("{:<"+ str(maxvalue_len+1)+"}{}  {}").format(
                            str(key)+":",
                            "{:7.3f}%".format(results[key]/count*100),
                            probs_str
                          ))
        else:
            print(("{:<"+ str(maxvalue_len+1)+"}{:7.3f}%  {}").format(
                        str(key)+":",
                        results[key]/count*100,
                        u"\u2588"*bar_length + " "*(total_bar_length-bar_length+1)
                      ))
    return len(results.values())

def print_instructions():
    print("usage: {} 'dice-math'".format(sys.argv[0]))
    print("usage: {} 'options:dice-math'".format(sys.argv[0]))
    print()
    print("Evaluate probabilistic dice math expressions.")
    print()
    print("Supported dice types:")
    print("- Regular dice '[R]dN'. Throws an N sided die R times.")
    print("- Fate dice '[R]F'. Throws a Fate die (-1,-1,0,0,1,1) R times.")
    print("Supported operators:")
    print("+, -, *, =, <, <=, >, =>")
    print("Also supports constant integers")
    print()
    print("Options:")
    print("- 'S', runs a statistical simulation instead of giving analytic results")
    print("- 'O', displays odds instead of a graph result")
    print("- 'C', displays the result in cumulative form")

def main(arg_string):
    try:
        instructions, calculation = arg_string.split(':')
    except ValueError:
        instructions, calculation = "", arg_string

    analytic = not "S" in instructions
    cumulative = "C" in instructions
    show_odds = "O" in instructions

    solve(calculation, report_cumulative=cumulative, analytic=analytic, show_odds=show_odds)

if __name__ == "__main__":
    try:
        if len(sys.argv[1:])==0:
            raise ValueError
        main(" ".join(sys.argv[1:]))
    except ValueError:
        print_instructions()

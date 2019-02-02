import sys
import re
import random
import shutil

import numexpr

class InputHandler:
    def __call__(self, input_string):
        match = re.search(self.regex, input_string)
        if match:
            return self(    input_string[:match.span()[0]] + \
                            str(self.output(match)) + \
                            input_string[match.span()[1]:])
        else:
            return input_string

class DiceHandler(InputHandler):
    def __init__(self):
        self.regex = "([0-9]*)d([1-9][0-9]*)"
    def output(self, match):
        if match.groups()[0]:
            repeats = int(match.groups()[0])
        else:
            repeats = 1
        dietype = int(match.groups()[1])
        return sum(random.randint(1,dietype) for i in range(repeats))

class FateDiceHandler(InputHandler):
    def __init__(self):
        self.regex = "([0-9]*)F"
    def output(self, match):
        if match.groups()[0]:
            repeats = int(match.groups()[0])
        else:
            repeats = 1
        return sum(random.randint(-1,1) for i in range(repeats))

def evaluate(input_string):
    literal_str = FateDiceHandler()(input_string)
    literal_str = DiceHandler()(literal_str)
    return numexpr.evaluate(literal_str)

def simulate(input_string, report_cumulative=False):
    results = {}
    count = 0
    try:
        while True:
            result = int(evaluate(input_string))
            count += 1
            try:
                results[result] += 1
            except KeyError:
                results[result] = 1

            if (count+1)%1000 == 0:
                print_height = print_graph(results, report_cumulative)
                print(f"\033[F"*(len(print_height)+2))
    except KeyboardInterrupt:
        print_graph(results, report_cumulative)
        return

def results_to_cumulative(results):
    sorted_keys = sorted(results.keys())
    cumulative = {sorted_keys[i]:sum(   results[j]
                                        for j in sorted_keys[:i+1])
                                        for i in range(len(sorted_keys))}
    return cumulative

def print_graph(results, cumulative=False):
    print("Expected value: {:6.3f}".format(sum((i/sum(results.values()))*results[i] for i in results)))

    if cumulative:
        results = results_to_cumulative(results)
        count = max(results.values())
    else:
        count = sum(results.values())

    maxvalue = max(results.values())
    maxvalue_len = max(len(str(i)) for i in results.keys())
    total_bar_length = shutil.get_terminal_size((80,20))[0]-maxvalue_len-12

    for key in sorted(results.keys()):
        bar_length = round(results[key]/maxvalue*total_bar_length)
        print(("{:<"+ str(maxvalue_len+1)+"}{:7.3f}%  {}").format(
                        str(key)+":",
                        results[key]/count*100,
                        u"\u2588"*bar_length + " "*(total_bar_length-bar_length+1)
                      ))
    return results.keys()

def main(arg_string):
    if arg_string[0] == "C":
        simulate(arg_string[1:], report_cumulative=True)
    else:
        simulate(arg_string, report_cumulative=False)

if __name__ == "__main__":
    main(" ".join(sys.argv[1:]))

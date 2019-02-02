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

def evaluate(input_string):
    literal_str = DiceHandler()(input_string)
    return numexpr.evaluate(literal_str)

def simulate(input_string):



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
                print_height = print_graph(results)
                print(f"\033[F"*(len(print_height)+2))
    except KeyboardInterrupt:
        print_graph(results)
        return

def print_graph(results):
    maxvalue = max(results.values())
    maxvalue_len = max(len(str(i)) for i in results.values())
    total_bar_length = shutil.get_terminal_size((80,20))[0]-maxvalue_len-12
    count = sum(results.values())

    print("Expected value: {:6.3f}".format(sum((i/count)*results[i] for i in results)))
    for key in sorted(results.keys()):
        bar_length = round(results[key]/maxvalue*total_bar_length)
        print(("{:<"+ str(maxvalue_len)+"}{:6.3f}%  {}").format(
                        str(key)+":",
                        results[key]/count*100,
                        u"\u2588"*bar_length + " "*(total_bar_length-bar_length+1)
                      ))
    return results.keys()

def main(arg_string):
    simulate(arg_string)

if __name__ == "__main__":
    main(" ".join(sys.argv[1:]))

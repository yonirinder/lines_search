import abc
from argparse import ArgumentParser
import re

import colorama


class ProcessData(object):
    metaclass = abc.ABCMeta

    @staticmethod
    def reade_data():
        if args.file:
            for i in args.file:
                with open(i, "r")as f:
                    content = f.readlines()
                yield i, content
        else:
            yield 'stdin', " ".join(args.stdin).split("\\n")

    @abc.abstractmethod
    def print_data(self):
        pass


class PrintData(ProcessData):

    def print_data(self):
        for file_name, content in self.reade_data():
            for row in range(len(content)):
                for _ in re.findall(args.regex, content[row]):
                    print(file_name, row)


class PrintDataUnderscore(ProcessData):

    def print_data(self):
        for file_name, content in self.reade_data():
            for line in content:
                print("".join(line))
                if re.findall(args.regex, line):
                    p = re.compile(args.regex)
                    for m in p.finditer(line):
                        result = [" " for _ in range(m.start())]
                        print("".join(result) + "^")


class PrintDataColor(ProcessData):

    def print_data(self):
        colorama.init()
        for file_name, content in self.reade_data():
            for line in content:
                colour_format = '\033[{0}m'
                colour_str = colour_format.format(32)
                reset_str = colour_format.format(0)
                last_match = 0
                formatted_text = ''
                for match in re.finditer(args.regex, line):
                    start, end = match.span()
                    formatted_text += line[last_match: start]
                    formatted_text += colour_str
                    formatted_text += line[start: end]
                    formatted_text += reset_str
                    last_match = end
                formatted_text += line[last_match:]
                print(formatted_text)


class PrintDataMachine(ProcessData):

    def print_data(self):
        for file_name, content in self.reade_data():
            file_name = '_'.join(file_name.split(" "))
            for line in content:
                for index, match in enumerate(re.findall(args.regex, line)):
                    print("file_name:{file}:start_pos:{pos}:matched_text:{text}".format(file=file_name, pos=index,
                                                                                        text=match))


parser = ArgumentParser()
parser.add_argument("-f", "--file", nargs='*',
                    help="select file/s")
parser.add_argument("stdin", nargs='*',
                    help="select file/s")
parser.add_argument("-r", "--regex", type=str,
                    dest="regex", required=True,
                    help="regex to find")
parser.add_argument("-u", "--underscore", action='store_true',
                    dest="underscore",
                    help="print with underscore")
parser.add_argument("-c", "--color", action='store_true',
                    dest="color",
                    help="print with color")
parser.add_argument("-m", "--machine", action='store_true',
                    dest="machine",
                    help="print machine readable")

args = parser.parse_args()

if args.underscore:
    PrintDataUnderscore().print_data()
elif args.color:
    PrintDataColor().print_data()
elif args.machine:
    PrintDataMachine().print_data()
else:
    PrintData().print_data()

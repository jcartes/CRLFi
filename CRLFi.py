#!/usr/bin/python3

from termcolor import colored
from urllib.parse import urlparse
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor

from lib.Send import Send
from lib.Engine import PayloadGenerator
from lib.PathFunctions import PathFunction
from lib.Globals import payloads, to_try, ColorObj
from lib.Functions import starter, write_output

parser = ArgumentParser(description=colored("CRLFi Scanner", color='yellow'), epilog=colored("Enjoy bug hunting",color='yellow'))
input_group = parser.add_mutually_exclusive_group()
output_group = parser.add_mutually_exclusive_group()
input_group.add_argument('---', '---', action="store_true", dest="stdin", help="Stdin")
input_group.add_argument('-w', '--wordlist', type=str, help="Wordlist")
parser.add_argument('-d', '--domain', type=str, help="Domain name")
output_group.add_argument('-o', '--output', type=str, help="Output file")
output_group.add_argument('-oD', '--output-directory', type=str, help="Output directory")
parser.add_argument('-t', '--threads', type=int, help="Number of threads")
parser.add_argument('-b', '--banner', action="store_true", help="Print banner and exit")
argv = parser.parse_args()

input_wordlist = starter(argv)
Sender = Send()
PathFunctioner = PathFunction()
Payloader = PayloadGenerator()

def async_generator(url: str):
    global to_try
    parsed_url = urlparse(PathFunctioner.urler(url))
    print_asyncgen = lambda data: print(f"{ColorObj.information} Generating {data} for: {colored(url, color='cyan')}")
    try:
        if parsed_url.query:
            print_asyncgen('query')
            for payloaded_url in Payloader.query_generator(parsed_url, payloads):
                to_try.append(payloaded_url)
            print_asyncgen('path')
            for payloaded_url in Payloader.path_generator(parsed_url, payloads):
                to_try.append(payloaded_url)
        elif parsed_url.path:
            print_asyncgen('path')
            for payloaded_url in Payloader.path_generator(parsed_url, payloads):
                to_try.append(payloaded_url)
        elif parsed_url.netloc:
            print_asyncgen('netloc')
            for payloaded_url in Payloader.netloc_generator(parsed_url, payloads):
               to_try.append(payloaded_url)
    except Exception as E:
        from traceback import print_exc, format_exc
        print_exc()
        format_exc()

try:
    with ThreadPoolExecutor(max_workers=argv.threads) as Mapper:
        async_generator(argv.domain)
        Mapper.map(async_generator, input_wordlist)
    with ThreadPoolExecutor(max_workers=argv.threads) as Submitter:
        future_objects = [Submitter.submit(Sender.sender_function, p) for p in to_try]
        def owrite(future_objects):
            if argv.output_directory:
                write_output(future_objects, filename = argv.domain, path = argv.output_directory)
            if argv.output:
                write_output(future_objects, filename = argv.output)
        owrite(future_objects)
except KeyboardInterrupt:
    exit()
except Exception as E:
    print(E,E.__class__)


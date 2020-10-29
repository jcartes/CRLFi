#!/usr/bin/python3

from termcolor import colored
from urllib.parse import urlparse
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor

from lib.Engine import Engine
from lib.PathFunctions import urler
from lib.Globals import payloads, to_try, Color
from lib.Functions import starter, write_output, send_payload

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
Payloader = Engine()

def async_generator(url: str):
    global to_try
    if not url:
        return []
    parsed_url = urlparse(urler(url))
    print_asyncgen = lambda data: print(f"{Color.information} Generating {data} for: {colored(url, color='cyan')}")
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
    except Exception:
        print(E,E.__class__)
try:
    with ThreadPoolExecutor(max_workers=argv.threads) as mapper:
        mapper.map(async_generator, input_wordlist)
    with ThreadPoolExecutor(max_workers=argv.threads) as submitter:
        objects = [submitter.submit(send_payload, payloaded_url) for payloaded_url in to_try]
        if argv.output_directory:
            write_output(objects, filename = argv.domain, path = argv.output_directory)
        elif argv.output:
            write_output(objects, filename = argv.output)
except KeyboardInterrupt:
    exit()
except Exception as E:
    print(E, E.__class__)


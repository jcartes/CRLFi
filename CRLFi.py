#!/usr/bin/python3

from termcolor import colored
from urllib.parse import urlparse
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor

from lib.Functions import request_to_try, starter
from lib.Functions import ColorObj, write_output
from lib.Globals import payloads, to_try
from lib.PathFunctions import PathFunction
from lib.PayloadGen import PayloadGenerator

parser = ArgumentParser(description=colored("CRLFi Finding Tool", color='yellow'), epilog=colored("Enjoy bug hunting",color='yellow'))
group = parser.add_mutually_exclusive_group()
group.add_argument('---', '---', action="store_true", dest="stdin", help="Stdin")
group.add_argument('-w', '--wordlist', type=str, help="Wordlist")
parser.add_argument('-d', '--domain', type=str, help="Domain name")
parser.add_argument('-oD', '--output-directory', type=str, help="Output directory")
parser.add_argument('-t', '--threads', type=int, help="Number of threads")
parser.add_argument('-b', '--banner', action="store_true", help="Print banner and exit")
argv = parser.parse_args()

input_wordlist = starter(argv)
FPathApp = PathFunction()
PayloaderApp = PayloadGenerator()

def async_generator(url: str):
    global to_try
    parsed_url = urlparse(FPathApp.urler(url))
    try:
        if parsed_url.query:
            print(f"{ColorObj.information} Generating query payload for: {colored(url, color='cyan')}")
            for payloaded_url in PayloaderApp.query_generator(parsed_url, payloads):
                to_try.append(payloaded_url)
            print(f"{ColorObj.information} Generating path payload for: {colored(url, color='cyan')}")
            for payloaded_url in PayloaderApp.path_generator(parsed_url, payloads):
                to_try.append(payloaded_url)
        elif parsed_url.path:
            print(f"{ColorObj.information} Generating path payload for: {colored(url, color='cyan')}")
            for payloaded_url in PayloaderApp.path_generator(parsed_url, payloads):
                to_try.append(payloaded_url)
        elif parsed_url.netloc:
            print(f"{ColorObj.information} Generating netloc payload for: {colored(url, color='cyan')}")
            for payloaded_url in PayloaderApp.netloc_generator(parsed_url, payloads):
               to_try.append(payloaded_url)
    except Exception as E:
        print(f"Error {E}, {E.__class__} failed async generator")

try:
    with ThreadPoolExecutor(max_workers=argv.threads) as Mapper:
        async_generator(argv.domain)
        Mapper.map(async_generator, input_wordlist)

    with ThreadPoolExecutor(max_workers=argv.threads) as Submitter:
        del PayloaderApp; del async_generator;
        print(f"{ColorObj.good} Freeing some memory..")
        future_objects = [Submitter.submit(request_to_try, payload_to_try) for payload_to_try in to_try]
        if argv.output_directory:
            write_output(argv.output_directory, argv.domain, future_objects)
except KeyboardInterrupt:
    exit()
except Exception as E:
    print(E,E.__class__)


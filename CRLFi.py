#!/usr/bin/python3
from termcolor import colored
from urllib.parse import urlparse
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor

from lib.Functions import request_to_try, starter, ColorObj
from lib.Globals import payloads, to_try
from lib.PathFunctions import PathFunction
from lib.PayloadGen import PayloadGenerator

parser = ArgumentParser(description=colored("CRLFi Finding Tool", color='yellow'), epilog=colored("Enjoy bug hunting",color='yellow'))
parser.add_argument('-w', '--wordlist', type=str, help="Absolute path of input file")
parser.add_argument('-oD', '--output-directory', type=str, help="Output file directory")
parser.add_argument('-d', '--domain', type=str, help="Domain name")
parser.add_argument('-t', '--threads', type=int, help="No of threads")
parser.add_argument('-b', '--banner', action="store_true", help="Print banner and exit")
argv = parser.parse_args()

starter(argv)
FPathApp = PathFunction()
PayloaderApp = PayloadGenerator(argv.domain)
input_wordlist = [line.rstrip('\n') for line in open(argv.wordlist)]
output_file = open(FPathApp.slasher(argv.output_directory) + argv.domain + '.CRLFi', 'a')

def async_generator(url: str):
    global to_try
    parsed_url = urlparse(FPathApp.urler(url))
    try:
        if parsed_url.query:
            print(f"{ColorObj.information} Generating query payload for: {colored(url, color='cyan')}")
            for payloads_full_url in PayloaderApp.query_generator(parsed_url, payloads):
                to_try.append(payloads_full_url)
            print(f"{ColorObj.information} Generating path payload for: {colored(url, color='cyan')}")
            for payloads_full_url in PayloaderApp.path_generator(parsed_url, payloads):
                to_try.append(payloads_full_url)
        elif parsed_url.path:
            print(f"{ColorObj.information} Generating path payload for: {colored(url, color='cyan')}")
            for payloads_full_url in PayloaderApp.path_generator(parsed_url, payloads):
                to_try.append(payloads_full_url)
        elif parsed_url.netloc:
            print(f"{ColorObj.information} Generating netloc payload for: {colored(url, color='cyan')}")
            for payloads_full_url in PayloaderApp.netloc_generator(parsed_url, payloads):
               to_try.append(payloads_full_url)
    except Exception as E:
        print(f"Error {E}, {E.__class__} failed async generator")

with ThreadPoolExecutor(max_workers=argv.threads) as Mapper:
    async_generator(argv.domain)
    try:
        Mapper.map(async_generator, input_wordlist)
    except KeyboardInterrupt:
        exit()
    except Exception as E:
        print(f"{ColorObj.bad} Error {E},{E.__class__} in Mapper")

with ThreadPoolExecutor(max_workers=argv.threads) as Submitter:
    try:
        print(f"{ColorObj.good} Freeing some memory..")
        del input_wordlist;del async_generator;del FPathApp;del PayloaderApp;del starter;del urlparse;del PathFunction;del PayloadGenerator
        del ArgumentParser;del argv;del parser;del payloads
    except Exception as E:
        print(E,E.__class__)
        f = open('/var/log/CRLFi', 'a')
        f.write(E,E.__class__)
        f.close()
    try:
        future_objects = [Submitter.submit(request_to_try, triable) for triable in to_try]
    except KeyboardInterrupt:
        print(f"{ColorObj.bad} Keyboard Interrupt Detected. Aborting")
        exit()
    except Exception as E:
        print(f"{ColorObj.bad} Exception {E},{E.__class__} occured")

    for future_object in future_objects:
        the_payload, is_exploitable = future_object.result()
        if is_exploitable:
            print(f"{ColorObj.good} Yes, the url is exploitable;Payload: {the_payload}")
        output_file.write("Exploitable:{}, Payload:{}\n".format(is_exploitable, the_payload))
        continue
    output_file.close()

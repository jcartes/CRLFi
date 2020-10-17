from sys import stdin
from termcolor import colored

from lib.PathFunctions import PathFunction
from lib.Globals import ColorObj, Headers

def banner():
    banner = '\x1b[5m\x1b[1m\x1b[40m\x1b[31m   __________  __    _______ \n  / ____/ __ \\/ /   / ____(_)\n / /   / /_/ / /   / /_  / / \n/ /___/ _, _/ /___/ __/ / /  \n\\____/_/ |_/_____/_/   /_/   \n                             \n\x1b[0m'
    print(banner)
    print(colored('Intelligent CRLFi Hunter', color='red', attrs=['bold']))
    exit()

def starter(argv):
    if argv.banner:
        banner()
    if argv.output_directory:
        if not argv.domain:
                print("{} Output directory specified but not domain".format(ColorObj.bad))
                exit()
    if not argv.wordlist:
        if not argv.domain:
            if not argv.stdin:
                print("{} Use --help".format(ColorObj.bad))
                exit()
            else:
                return [line.rstrip('\n').strip(' ') for line in stdin.read().split('\n') if line]
        else:
            return [argv.domain.strip(' ')]
    else:
        return [line.rstrip('\n') for line in open(argv.wordlist)]

def write_output(objects, filename = None, path = None):
    if path:
        path_fn = PathFunction()
        output_file = open(path_fn.ender(path, '/') + filename + '.CRLFi', 'a')
    elif filename:
        output_file = open(filename, 'a')
    else:
        assert False, "The program errored out"
    for future_object in objects:
        the_payload, is_exploitable = future_object.result()
        if is_exploitable:
            print(f"{ColorObj.good} Yes, the url is exploitable\t,Payload: {the_payload}")
        output_file.write("Exploitable:{}, Payload:{}\n".format(is_exploitable, the_payload))
    return output_file.close()     

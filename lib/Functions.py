from sys import stdin
from termcolor import colored

from lib.Globals import Color
from lib.PathFunctions import ender

def banner():
    b = '\x1b[5m\x1b[1m\x1b[40m\x1b[31m   __________  __    _______ \n  / ____/ __ \\/ /   / ____(_)\n / /   / /_/ / /   / /_  / / \n/ /___/ _, _/ /___/ __/ / /  \n\\____/_/ |_/_____/_/   /_/   \n                             \n\x1b[0m'
    print(b)
    print(colored('Intelligent CRLFi Hunter', color='red', attrs=['bold']))
    exit()

def starter(argv):
    if argv.banner:
        banner()
    if argv.output_directory:
        if not argv.domain:
            print("{} Output directory specified but not domain".format(Color.bad))
            exit()
    if not argv.wordlist:
        if not argv.domain:
            if not argv.stdin:
                print("{} Use --help".format(Color.bad))
                exit()
            else:
                return (line.rstrip('\n').strip(' ') for line in stdin.read().split('\n') if line)
        else:
            return [argv.domain.strip(' ')]
    else:
        return (line.rstrip('\n') for line in open(argv.wordlist) if line)

def write_output(objects, filename=None, path=None):
    if path:
        output_file = open(ender(path, '/') + filename + '.CRLFi', 'a')
    elif filename:
        output_file = open(filename, 'a')
    else:
        print("The program errored out")
        exit()
    for single_object in objects:
        the_payload, is_exploitable = single_object.result()
        if is_exploitable:
            print(f"{Color.good} Yes, the url is exploitable\t,Payload: {the_payload}")
        output_file.write("Exploitable:{}, Payload:{}\n".format(is_exploitable, the_payload))
    return output_file.close()

from sys import stdin
from random import randint
from termcolor import colored
from requests import Session
from requests.exceptions import ConnectionError, Timeout

from lib.Globals import Color
from lib.PathFunctions import ender

s = Session()
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
                return (line.rstrip('\n') for line in stdin.read().split('\n') if line)
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
        print("Cant write output")
    for single_object in objects:
        the_payload, is_exploitable = single_object.result()
        if is_exploitable:
            print(f"{Color.good} Yes, the url is exploitable\t,Payload: {the_payload}")
        output_file.write("Exploitable:{}, Payload:{}\n".format(is_exploitable, the_payload))
    return output_file.close()

def deliver_request(url):
    r = randint(0, 1)
    isReturnable = False
    display_error = lambda error: f"{Color.bad} Skipping url due to {error}"
    print(f"{Color.information} Trying {colored(url, color='cyan')} against web server!")
    try:
        if r:
            response = s.get(url, timeout=5)
        elif not r:
            response = s.head(url, timeout=5)
    except ConnectionError:
        print(display_error("ConnectionError"))
        isReturnable = True
        return url, False, isReturnable
    except Timeout:
        print(display_error("TimeoutError"))
        isReturnable = True
        return url, False, isReturnable
    except Exception as E:
        print(display_error("OtherError"))
        isReturnable = True
        return url, False, isReturnable
    try:
        print(f"{Color.good} Response header: {response.headers['evil-here']}")
        isReturnable = True
        return url, True, isReturnable
    except:
        try:
            print(f"{Color.good} Response Cookie: {response.cookies['bugbounty']}")
            isReturnable = True
            return url, True, isReturnable
        except:
            return url, False, isReturnable

def send_payload(url: str) -> tuple:
    isReturnable = False
    url, exploitable, isReturnable  = deliver_request(url)
    if isReturnable:
        return url, exploitable
    instantiated_url = url.replace('http://', 'https://')
    url, exploitable, isReturnable = deliver_request(instantiated_url)
    if isReturnable:
        return instantiated_url, exploitable 
    instantiated_url = url.replace('http://', 'http://www.')
    url, exploitable, isReturnable = deliver_request(instantiated_url)
    if isReturnable:
        return instantiated_url, exploitable

from sys import stdin
from requests import Session   
from termcolor import colored
from random import randint as rdi
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError

from lib.Globals import ColorObj, Headers

def banner():
    from pyfiglet import print_figlet as puff
    puff('CRLF Injector', font='larry3d', colors='BLUE')
    print(colored('A smart CRLF Injector, which can inject CRLF in path, parameter and netloc!', color='red', attrs=['bold']))
    print(colored('It intelligently fuzzes in parameters and path', color='red', attrs=['bold']))

def starter(argv):
    if argv.banner:
        banner()
        exit(0)
    if argv.output_directory:
        if not argv.domain:
                print("{} Output directory specified but not domain".format(ColorObj.bad))
                exit()
    if not argv.wordlist:
        if not domain:
            if not argv.stdin:
                print("{} Use --help".format(ColorObj.bad))
                exit()
            else:
                stdinarray = stdin.read().split('\n')
                return [line.rstrip('\n').strip(' ') for line in stdinarray if line]
        else:
            return [argv.domain.strip(' ')]
    else:
        return [line.rstrip('\n') for line in open(argv.wordlist)]
                

def request_to_try(url: str) -> tuple:
    print(f"{ColorObj.information} Trying {colored(url, color='cyan')} against web server!")
    isReturnable = False
    s = Session()
    try:
        if rdi(0,1) == 0:
            response = s.get(url, timeout=8)
        elif rdi(0,1) == 1:
            response = s.head(url, timeout=8, headers=Headers)
        else:
            response = s.head(url, timeout=8)
    except ConnectionError:
        print(f"{ColorObj.bad} Cant connect to url: {url}")
        return url, False
    except Timeout:
        print(f"{ColorObj.bad} Coudlnt connect in time: {url}")
        return url, False
    except Exception as E:
        print(f"{ColorObj.bad} Exception {E},{E.__class__} occured")
        return url, False
    
    try:
        print(f"{ColorObj.good} Response header: {response.headers['evil-here']}")
        isReturnable = True
    except:
        pass
    try:
        print(f"{ColorObj.good} Response Cookie: {response.cookies['bugbounty']}")
        isReturnable = True
    except:
        pass 
    
    if isReturnable:
        return url, True
    
    ssl_url = url.replace('http://', 'https://')
    print(f"{ColorObj.information} Trying {colored(ssl_url, color='cyan')} against web server!")
    try:
        if rdi(0,1) == 0:
            response = s.get(ssl_url, timeout=8, headers=Headers)
        elif rdi(0,1) == 1:
            response = s.head(ssl_url, timeout=8)
        else:
            response = s.head(ssl_url, timeout=8)
    except ConnectionError:
        print(f"{ColorObj.bad} Cant connect to url: {ssl_url}")
        return ssl_url, False
    except Timeout:
        print(f"{ColorObj.bad} Coudlnt connect in time: {ssl_url}")
        return ssl_url, False
    except Exception as E:
        print(f"{ColorObj.bad} Exception {E},{E.__class__} occured")
        return ssl_url, False

    try:
        print(f"{ColorObj.good} Response header: {response.headers['evil-here']}")
        isReturnable = True
    except:
        pass
    try:
        print(f"{ColorObj.good} Response Cookie: {response.cookies['bugbounty']}")
        isReturnable = True
    except:
        pass 
    if isReturnable:
        return ssl_url, True 
    if 'www.' in ssl_url:
        print(f"{ColorObj.other} www already exist in url {url}")
        return url, False
    if url.count('.') >= 2:
        print(f"{ColorObj.other} Skipping www for subdomain {url}")
        return url, False
    try:
        ssl_url = None
        if rdi(0,100) < 36:
            www_url = url.replace('http://', 'https://www.')
        else:
            www_url = url.replace('http://', 'http://www.')
        print(f"{ColorObj.information} Trying {colored(www_url, color='cyan')} against web server!")
        try:
            if rdi(0,1) == 0:
                response = s.get(www_url, timeout=8)
            else:
                response = s.head(www_url, timeout=8, headers=Headers)
        except ConnectionError:
            print(f"{ColorObj.bad} Cant connect to url: {www_url}")
            return www_url, False
        except Timeout:
            print(f"{ColorObj.bad} Cant connect to url: {www_url}")
            return www_url, False
        except Exception as E:
            print(f"{ColorObj.bad} Exception {E}, {E.__class__} occured")
            return www_url, False
        try:
            print(f"{ColorObj.good} Response header: {response.header['evil-here']}")
            isReturnable = True
        except:
            pass
        try:
            print(f"{ColorObj.good} Response header: {response.cookies['bugbounty']}")
            isReturnable = True
        except:
            pass
        if isReturnable:
            return www_url, True
    except Exception as E:
        print(f"{ColorObj.bad} Unexpected error {E},{E.__class__} in request to try function")
    return url, False

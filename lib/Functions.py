from termcolor import colored
from lib.Globals import ColorObj

def banner():
    from pyfiglet import print_figlet as puff
    puff('CRLF Injector', font='larry3d', colors='BLUE')
    print(colored('CRLF injection in path, parameter and netlocs!', color='red', attrs=['bold']))

def starter(argv):
    if argv.banner:
        banner()
        exit(0)
    if not argv.wordlist or not argv.domain or not argv.output_directory or not argv.threads:
        print("{} Use --help".format(ColorObj.bad))
        exit()

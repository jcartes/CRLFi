from re import findall,search
from requests import Session
from requests.exceptions  import ConnectionError, Timeout
from termcolor import colored
from random import randint as rdi

from lib.PathFunctions import PathFunction
from lib.Globals import ColorObj
from lib.ParamReplacer import ParamReplace
from lib.PathFuzzer import PathFuzz
from lib.Skipper import Skip

class PayloadGenerator:
    def __init__(self, domain: str):
        self.FPathApp = PathFunction()
        self.ReplacerApp = ParamReplace()
        self.Skipper = Skip()
        self.PathApp = PathFuzz()
        self.s = Session()
        self.error = self.netloc_error(domain)
        print(f"{ColorObj.other} Error number for {colored(domain, color='cyan')} is: {colored(self.error, color='red')}")
    
    def query_generator(self, parsed_url: str, payloads: list) -> list:
        try:
            NotTried, ToTry = [], []
            upto_path = self.FPathApp.slasher(self.FPathApp.urler(parsed_url.netloc)) + self.FPathApp.payloader(parsed_url.path) 
            query = parsed_url.query
            if len(query) > 550:
                return ToTry
            parameters, values = self.ReplacerApp.expand_parameter(query)
            for parameter in parameters:
                if not self.Skipper.check_parameter(upto_path, parameter):
                    self.Skipper.add_parameter(upto_path, [parameter])
                else:
                    print(f"{ColorObj.bad} Skipping some used parameters.")
                    continue 
                if not self.Skipper.check_unique_parameter(parameter):
                    self.Skipper.add_unique_parameter([parameter])
                else:
                    print(f"{ColorObj.bad} Skipping some largely used parameters.")
                    continue
                NotTried.append(parameter)
            if not len(NotTried):
                return ToTry
            for payload in payloads:
                QueryList = self.ReplacerApp.only_replacement(parameters, values, self.FPathApp.payloader(payload), NotTried)
                PayloadsList = self.ReplacerApp.gen_url(upto_path, QueryList)
                [ToTry.append(TriablePayloads) for TriablePayloads in PayloadsList]
            return ToTry
        except Exception as E:
            print(f"{ColorObj.bad} Exception in Query generator: {E},{E.__class__}")

    def path_generator(self, parsed_url: str, payloads: list) -> list:
        try:
            ToTry = []
            upto_path = self.FPathApp.slasher(self.FPathApp.urler(parsed_url.netloc)) 
            if parsed_url.path == '/' or len(parsed_url.path) == 1:
                PayloadsList = self.netloc_generator(parsed_url, payloads)
                ToTry = [payloads for payloads in PayloadsList]
                return ToTry
            else:
                PathList = [str(path + '/') for path in findall(r'([^/]+)', parsed_url.path)]
                PathListLen = len(PathList) -1 
                PathListRange = range(PathListLen, 0, -1)
                for i in PathListRange:
                    unslashed = self.FPathApp.unslasher(PathList[i-1])
                    if self.Skipper.check_path(PathList[i-1]):
                        print(f"{ColorObj.bad} Skipping some used paths.")
                        return ToTry
                    elif search('[a-zA-Z].+[0-9]$', unslashed):
                        print(f"{ColorObj.bad} Skipping some numbered paths.")
                        return ToTry
                    elif search('^[0-9].*$', unslashed) and len(unslashed) >= 2:
                        print(f"{ColorObj.bad} Skipping some more more numbered paths.")
                        return ToTry
                    elif not self.Skipper.check_path(PathList[i-1]):
                        self.Skipper.add_path(PathList[i-1])    
                    for payload in payloads:
                        PathList[i] = self.FPathApp.payloader(payload)
                        path_payload = upto_path + "".join(PathList)
                        ToTry.append(path_payload)
                    PathList.pop()
                return ToTry
        except Exception as E:
            print(f"{ColorObj.bad} Exception in Path generator: {E},{E.__class__}")

    def netloc_generator(self, parsed_url: str, payloads: list) -> list:
        try:
            ToTry = []
            if parsed_url.netloc.count('.') >= 5 or len(parsed_url.netloc) > 40:
                print(f"{ColorObj.bad} Skipping url {colored(parsed_url.netloc, color='cyan')}!")
                return ToTry
            netloc_error = self.netloc_error_checker(parsed_url)
            if netloc_error:
                print(f"{ColorObj.bad} Skipping url {colored(parsed_url.netloc, color='cyan')} due to error page!")
                return ToTry
            try:
                netdata = self.s.get(self.FPathApp.urler(parsed_url.netloc), timeout=6, allow_redirects=True)
                if netdata.status_code == 404:
                    if self.error == -1:
                        self.error = self.netloc_error(parsed_url.netloc)  
            except ConnectionError:
                print(f"{ColorObj.bad} Cant connect to {parsed_url.netloc}. Skipping netloc payloads generation")
                return ToTry
            except Timeout:
                print(f"{ColorObj.bad} Connection timeout {parsed_url.netloc}. Skipping netloc payloads generation")
                return ToTry
            except Exception as E:
                print(f"{ColorObj.bad} Netloc error {E},{E.__class__} occured")
                pass
            if  self.Skipper.check_netloc(parsed_url.netloc):
                print(f"{ColorObj.bad} Skipping some used netloc")
                return ToTry
            else:
                self.Skipper.add_netloc(parsed_url.netloc)

            for payload in payloads:
                temp_pay = self.FPathApp.urler(self.FPathApp.slasher(parsed_url.netloc))
                ToTry.append(self.PathApp.FuzzPath(temp_pay, payload))
            return ToTry
        except Exception as E:
            print(f"{ColorObj.bad} Exception in Netloc generator: {E},{E.__class__}")

    def netloc_error(self, domain_only: str, skip=False) -> int:
        try:
            if not skip:
                domain = self.FPathApp.slasher(self.FPathApp.urler("psychopath." + domain_only))
            elif skip:
                domain = self.FPathApp.slasher(self.FPathApp.urler(domain_only))
            try: 
                response = self.s.head(self.FPathApp.slasher(domain), timeout=8, allow_redirects=True)
            except ConnectionError:
                print(f"{ColorObj.other} Cant determine error page!")
                return -1
            if response.status_code == 404:
                return response.reason
        except Exception as E:
            print(E,E.__class__)

    def netloc_error_checker(self, parsed_url: str) -> bool:
        try:
            if self.error == -1:
                return False
            try:
                response = self.s.head(self.FPathApp.urler(self.FPathApp.slasher(parsed_url.netloc)), allow_redirects=True, timeout=8)
            except Exception as E:
                print(f"{ColorObj.bad} Error {E},{E.__class__} occured. Cant connect")
                return True
            if response.status_code == 404:
                if response.reason == self.error:
                    return True
            else:
                return False
        except Exception as E:
            print(E,E.__class__)

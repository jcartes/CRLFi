from re import findall
from re import search
from requests import head
from termcolor import colored
from requests.exceptions import ConnectionError, Timeout

from lib.Globals import ColorObj
from lib.Skipper import Skip
from lib.PathFunctions import PathFunction
from lib.ParamReplacer import ParamReplace

class PayloadGenerator:
    def __init__(self):
        self.PathFunctioner = PathFunction()
        self.Replacer = ParamReplace()
        self.Skipper = Skip()
    
    def query_generator(self, parsed_url, payloads: list) -> list:
        try:
            parameters_to_try, payloads_to_try = [], []
            upto_path, query = self.PathFunctioner.merge(parsed_url.netloc, parsed_url.path), parsed_url.query
            if len(query) > 550: return payloads_to_try
            parameters, values = self.Replacer.expand_parameter(query)
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
                parameters_to_try.append(parameter)
            if not len(parameters_to_try): return payloads_to_try
            for payload in payloads:
                query_list = self.Replacer.only_replacement(parameters, values, self.PathFunctioner.unstarter(payload, '/'), parameters_to_try)
                payloads_list = self.Replacer.generate_url(upto_path, query_list)
                [payloads_to_try.append(p) for p in payloads_list]
            return payloads_to_try
        except Exception as E:
            print(f"{ColorObj.bad} Exception in Query generator: {E},{E.__class__}")

    def path_generator(self, parsed_url, payloads: list) -> list:
        try:
            payloads_to_try = []
            upto_path = self.PathFunctioner.urlerslasher(parsed_url.netloc)
            if parsed_url.path == '/' or len(parsed_url.path) == 1:
                payloads_list = self.netloc_generator(parsed_url, payloads)
                payloads_to_try = [payloads for payloads in payloads_list]
                return payloads_to_try
            else:
                path_list = [self.PathFunctioner.ender(path, '/') for path in findall(r'([^/]+)', parsed_url.path)]
                path_range = range(int(len(path_list) -1), 0, -1)
                for i in path_range:
                    unslashed = self.PathFunctioner.unender(path_list[i-1], '/')
                    if self.Skipper.check_path(path_list[i-1]):
                        print(f"{ColorObj.bad} Skipping some used paths.")
                        return payloads_to_try
                    elif search('[a-zA-Z].+[0-9]$', unslashed):
                        print(f"{ColorObj.bad} Skipping some numbered paths.")
                        return payloads_to_try
                    elif search('^[0-9].*$', unslashed) and len(unslashed) >= 2:
                        print(f"{ColorObj.bad} Skipping some more more numbered paths.")
                        return payloads_to_try
                    elif not self.Skipper.check_path(path_list[i-1]):
                        self.Skipper.add_path(path_list[i-1])    
                    for payload in payloads:
                        path_list[i] = self.PathFunctioner.payloader(payload)
                        path_payload = upto_path + "".join(path_list)
                        payloads_to_try.append(path_payload)
                    path_list.pop()
                return payloads_to_try
        except Exception as E:
            print(f"{ColorObj.bad} Exception in Path generator: {E},{E.__class__}")

    def netloc_generator(self, parsed_url, payloads: list) -> list:
        try:
            payloads_to_try = []
            if parsed_url.netloc.count('.') >= 5 or len(parsed_url.netloc) > 40:
                print(f"{ColorObj.bad} Skipping url {colored(parsed_url.netloc, color='cyan')}!")
                return payloads_to_try
            try:
                head(self.PathFunctioner.urler(parsed_url.netloc), timeout=5)
            except ConnectionError:
                print("{ColorObj.bad} Could not connect! {E}, {E.__class__} occured")
                return payloads_to_try
            except Timeout:
                print("{ColorObj.bad Timed out.Error occured: {E}")
                return payloads_to_try
            except Exception as E:
                print(f"{ColorObj.bad} Other connection error in netloc {E},{E.__class__} occured")
            if self.Skipper.check_netloc(parsed_url.netloc):
                print(f"{ColorObj.bad} Skipping some used netloc")
                return payloads_to_try
            else:
                self.Skipper.add_netloc(parsed_url.netloc)
            [payloads_to_try.append(self.PathFunctioner.merge(parsed_url.netloc, payload)) for payload in payloads]
            return payloads_to_try
        except Exception as E:
            print(f"{ColorObj.bad} Exception in Netloc generator: {E},{E.__class__}")

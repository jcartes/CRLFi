from termcolor import colored
from re import search, findall
from faster_than_requests import get2str

from lib.Skipper import Skip
from lib.Globals import ColorObj
from lib.PathFunctions import PathFunction
from lib.ParamReplacer import ParamReplace

class PayloadGenerator:
    def __init__(self):
        self.PathFunctions = PathFunction()
        self.Replacer = ParamReplace()
        self.Skipper = Skip()
    
    def query_generator(self, parsed_url, payloads: list) -> list:
        skip_print = f"{ColorObj.bad} Skipping some used parameters."
        parameters_to_try, payloads_to_try = [], []
        upto_path, query = self.PathFunctions.merge(parsed_url.netloc, parsed_url.path), parsed_url.query
        if len(query) > 550: return payloads_to_try
        parameters, values = self.Replacer.expand_parameter(query)
        for parameter in parameters:
            if not self.Skipper.check_parameter(upto_path, parameter):
                self.Skipper.add_parameter(upto_path, [parameter])
            else:
                print(skip_print)
                continue 
            if not self.Skipper.check_unique_parameter(parameter):
                self.Skipper.add_unique_parameter([parameter])
            else:
                print(skip_print)
                continue
            parameters_to_try.append(parameter)
        if not len(parameters_to_try): return payloads_to_try
        for payload in payloads:
            query_list = self.Replacer.only_replacement(parameters, values, self.PathFunctions.unstarter(payload, '/'), parameters_to_try)
            payloads_list = self.Replacer.generate_url(upto_path, query_list)
            [payloads_to_try.append(p) for p in payloads_list]
        return payloads_to_try

    def path_generator(self, parsed_url, payloads: list) -> list:
        payloads_to_try = []
        skip_print = f"{ColorObj.bad} Skipping some used paths."
        upto_path = self.PathFunctions.urlerslasher(parsed_url.netloc)
        if parsed_url.path == '/' or len(parsed_url.path) == 1:
            payloads_list = self.netloc_generator(parsed_url, payloads)
            payloads_to_try = [p for p in payloads_list]
        else:
            path_list = [self.PathFunctions.ender(path, '/') for path in findall(r'([^/]+)', parsed_url.path)]
            path_range = range(int(len(path_list) -1), 0, -1)
            for npath in path_range:
                unslashed = self.PathFunctions.unender(path_list[npath-1], '/')
                if self.Skipper.check_path(path_list[npath-1]):
                    print(skip_print)
                    return payloads_to_try
                elif search('[a-zA-Z].+[0-9]$', unslashed):
                    print(skip_print)
                    return payloads_to_try
                elif search('^[0-9].*$', unslashed) and len(unslashed) >= 2:
                    print(skip_print)
                    return payloads_to_try
                elif not self.Skipper.check_path(path_list[npath-1]):
                    self.Skipper.add_path(path_list[npath-1])    
                for payload in payloads:
                    path_list[npath] = self.PathFunctions.unstarter(payload, '/')
                    path_payload = upto_path + "".join(path_list)
                    payloads_to_try.append(path_payload)
                path_list.pop()
        return payloads_to_try

    def netloc_generator(self, parsed_url, payloads: list) -> list:
        error_print = lambda e: f"{ColorObj.bad} Skipping payload generation due to: {e}"
        skip_print = f"{ColorObj.bad} Skipping URL {colored(parsed_url.netloc, color='cyan')}!"
        if parsed_url.netloc.count('.') >= 5 or len(parsed_url.netloc) > 40:
            print(skip_print)
            return []
        if self.Skipper.check_netloc(parsed_url.netloc):
            print(skip_print)
            return []
        else:
            self.Skipper.add_netloc(parsed_url.netloc)
        try:
            get2str(self.PathFunctions.urler(parsed_url.netloc))
        except Exception as E:
            error = True
            e = E.__class__.__name__
            if e == "TimeoutError":
                print(error_print("Request Timeout"))
            elif e == "OSError":
                print(error_print("Connection Error"))
            elif e == "HttpRequestError":
                if '404' in str(E):
                    error = False
                else:
                    print(E)
            else:
                print(e)
            if error:
                return []
        return [self.PathFunctions.merge(parsed_url.netloc, payload) for payload in payloads if payload]

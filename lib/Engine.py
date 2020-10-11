from re import findall
from re import search
from termcolor import colored
from faster_than_requests import head

from lib.PathFunctions import PathFunction
from lib.Globals import ColorObj
from lib.ParamReplacer import ParamReplace
from lib.Skipper import Skip

class PayloadGenerator:
    def __init__(self):
        self.path_fn = PathFunction()
        self.ReplacerApp = ParamReplace()
        self.Skipper = Skip()
    
    def query_generator(self, parsed_url: str, payloads: list) -> list:
        try:
            parameters_to_try, payloads_to_try = [], []
            upto_path, query = self.path_fn.urlerslasher(parsed_url.netloc) + self.path_fn.payloader(parsed_url.path), parsed_url.query
            if len(query) > 550:
                return payloads_to_try
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
                parameters_to_try.append(parameter)
            if not len(parameters_to_try):
                return payloads_to_try
            for payload in payloads:
                query_list = self.ReplacerApp.only_replacement(parameters, values, self.path_fn.payloader(payload), parameters_to_try)
                PayloadsList = self.ReplacerApp.gen_url(upto_path, query_list)
                [payloads_to_try.append(TriablePayloads) for TriablePayloads in PayloadsList]
            return payloads_to_try
        except Exception as E:
            print(f"{ColorObj.bad} Exception in Query generator: {E},{E.__class__}")

    def path_generator(self, parsed_url: str, payloads: list) -> list:
        try:
            payloads_to_try = []
            upto_path = self.path_fn.urlerslasher(parsed_url.netloc)
            if parsed_url.path == '/' or len(parsed_url.path) == 1:
                PayloadsList = self.netloc_generator(parsed_url, payloads)
                payloads_to_try = [payloads for payloads in PayloadsList]
                return payloads_to_try
            else:
                PathList = [str(path + '/') for path in findall(r'([^/]+)', parsed_url.path)]
                PathListLen = len(PathList) -1 
                PathListRange = range(PathListLen, 0, -1)
                for i in PathListRange:
                    unslashed = self.path_fn.unslasher(PathList[i-1])
                    if self.Skipper.check_path(PathList[i-1]):
                        print(f"{ColorObj.bad} Skipping some used paths.")
                        return payloads_to_try
                    elif search('[a-zA-Z].+[0-9]$', unslashed):
                        print(f"{ColorObj.bad} Skipping some numbered paths.")
                        return payloads_to_try
                    elif search('^[0-9].*$', unslashed) and len(unslashed) >= 2:
                        print(f"{ColorObj.bad} Skipping some more more numbered paths.")
                        return payloads_to_try
                    elif not self.Skipper.check_path(PathList[i-1]):
                        self.Skipper.add_path(PathList[i-1])    
                    for payload in payloads:
                        PathList[i] = self.path_fn.payloader(payload)
                        path_payload = upto_path + "".join(PathList)
                        payloads_to_try.append(path_payload)
                    PathList.pop()
                return payloads_to_try
        except Exception as E:
            print(f"{ColorObj.bad} Exception in Path generator: {E},{E.__class__}")

    def netloc_generator(self, parsed_url: str, payloads: list) -> list:
        try:
            payloads_to_try = []
            if parsed_url.netloc.count('.') >= 5 or len(parsed_url.netloc) > 40:
                print(f"{ColorObj.bad} Skipping url {colored(parsed_url.netloc, color='cyan')}!")
                return payloads_to_try
            try:
                head(self.path_fn.urler(parsed_url.netloc), timeout=5000)
            except Exception as E:
                if str(E.__class__) == "<class 'nimpy.OSError'>":
                    print("{ColorObj.bad} Could not connect! {E}, {E.__class__} occured")
                    return payloads_to_try
                elif str(E.__class__) == "<class 'nimpy.TimeoutError'>":
                    print("{ColorObj.bad Timed out.Error occured: {E}")
                    return payloads_to_try
                else:
                    print(f"{ColorObj.bad} Other connection error in netloc {E},{E.__class__} occured")
            if  self.Skipper.check_netloc(parsed_url.netloc):
                print(f"{ColorObj.bad} Skipping some used netloc")
                return payloads_to_try
            else:
                self.Skipper.add_netloc(parsed_url.netloc)
            for payload in payloads:
                temp_payload = self.path_fn.urlerslasher(parsed_url.netloc)
                payloads_to_try.append(self.path_fn.merge(temp_payload, payload))
            return payloads_to_try
        except Exception as E:
            print(f"{ColorObj.bad} Exception in Netloc generator: {E},{E.__class__}")

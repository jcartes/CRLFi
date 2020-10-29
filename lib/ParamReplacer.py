from re import findall

from lib.PathFunctions import ender
class ParamReplace:
    def __init__(self):
        pass
    
    def replacement(self, parameter: list, value: list, replace_str: str) -> list:
        c_counter  = []
        returner_list = []
        counter = 0
        length = len(parameter)
        while counter != length:
            temp = value[counter]
            for i in range(length):
                value[counter] = replace_str
                c_counter.append(parameter[i] + '=' + value[i])
            returner_list.append(c_counter)
            value[counter] = temp
            counter += 1
            c_counter = []
        return returner_list
    
    def only_replacement(self, parameter: list, value: list, replace_str: str, only: list) -> list:
        returner_list = []
        c_counter  = []
        counter = 0
        length = len(parameter)
        while counter != length:
            temp = value[counter]
            for index in range(length):
                value[counter] = replace_str
                if parameter[index] in only:
                    c_counter.append(parameter[index] + '=' + value[index])
            returner_list.append(c_counter)
            value[counter] = temp
            counter += 1
            c_counter = []
        x_counter = []
        for item in returner_list:
            shit = [yyy.split('=')[-1] for yyy in item]
            if replace_str in shit:
                x_counter.append(item)
        return x_counter


    def generate_url(self, half_url: str, parameters: list) -> list:
        return [ender(half_url, '?') + '&'.join(parameter) for parameter in parameters]

    def expand_parameter(self, query_data: str) -> tuple:
        p,q = [],[]
        for parameters,values in findall(r'([^&]+)=([^&]+)', query_data):
            p.append(parameters)
            q.append(values)
        if len(p) != len(q):
            return False,False
        return p,q

    def auto(self, upto_path_url, parameter_to_expand, payload):
        parameter, value = self.expand_parameter(parameter_to_expand)
        xpath = self.replacement(parameter, value, payload)
        ypath = self.generate_url(upto_path_url, xpath)
        return ypath

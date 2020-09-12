class ParamReplace:
    def __init__(self):
        pass
    
    def replacement(self, parameter: list, value: list, replace_str: str) -> list:
        c_counter  = []
        returner_list = []
        counter = 0
        while counter != len(parameter):
            temp = value[counter]
            for i in range(len(parameter)):
                value[counter] = replace_str
                c_counter.append(parameter[i] + '=' + value[i])
            returner_list.append(c_counter)
            value[counter] = temp
            counter += 1
            c_counter = []
        return returner_list
    
    def only_replacement(self, parameter: list, value: list, replace_str: str, only: list) -> list:
        c_counter  = []
        returner_list = []
        counter = 0
        while counter != len(parameter):
            temp = value[counter]
            for i in range(len(parameter)):
                value[counter] = replace_str
                if parameter[i] in only:
                    c_counter.append(parameter[i] + '=' + value[i])
            returner_list.append(c_counter)
            value[counter] = temp
            counter += 1
            c_counter = []
        x_counter = []
        for xxx in returner_list:
            shit = [yyy.split('=')[-1] for yyy in xxx]
            if replace_str in shit:
                x_counter.append(xxx)
        return x_counter


    def gen_url(self, half_url: str, xdata: str) -> list:
        returner_list = []
        for each in xdata:
            if half_url[-1] != "?":
                returner_list.append(half_url + '?' + str("&".join(each)))
            else:
                returner_list.append(half_url + str("&".join(each)))
        return returner_list

    def expand_parameter(self, query_data: str) -> tuple:
        from re import findall
        p,q = [],[]
        for parameters,values in findall(r'([^&]+)=([^&]+)', query_data):
            p.append(parameters)
            q.append(values)
        if len(p) != len(q):
            return False,False
        return p,q

    def auto(self, upto_path_url, ppath, payload):
        apath, bpath = self.expand_parameter(ppath)
        xpath = self.replacement(apath, bpath, payload)
        ypath = self.gen_url(upto_path_url, xpath)
        return ypath

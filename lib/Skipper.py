from lib.PathFunctions import PathFunction

class Skip:
    def __init__(self):
        self.exist = False 
        self.path_list = []
        self.netloc_list = []
        self.parameter_list = {}
        self.uparameter_list = {}
        self.path_fn = PathFunction()

    def add_path(self, path_to_add: str) -> bool:
        if path_to_add in self.path_list:
            return False
        else:
            self.path_list.append(path_to_add)
            return True

    def add_parameter(self, url: str, parameter_list: list) -> list:
        url = self.path_fn.ender(url, '?')
        if url in self.parameter_list:
             var = self.parameter_list[url]
             var.update(set(parameter_list))
             self.parameter_list[url] = var
        else:
             self.parameter_list[url] = set(parameter_list)
        return self.parameter_list[url] 
    
    def add_unique_parameter(self, parameter_list: list) -> bool:
        for parameter in parameter_list:
            if not parameter in self.uparameter_list:
                self.uparameter_list[parameter] = 0
            else:
                self.uparameter_list[parameter] += 1
        return True
 
    def add_netloc(self, netloc: str) -> bool:
        if netloc in self.netloc_list:
            return False
        else:
            self.netloc_list.append(netloc)
            return True

    def check_path(self, path_to_add: str) -> bool: #return True if found
        if path_to_add in self.path_list:
            return True
        else:
            return False

    def check_netloc(self, netloc: str) -> bool: #return True if found
        if netloc in self.netloc_list:
            return True
        else:
            return False

    def check_parameter(self, url: str, parameter: str) -> bool: #return True if found
        url = self.path_fn.ender(url, '?')
        try:
            if self.parameter_list[url]:
                self.exist = True
        except:
            self.exist = False
        if self.exist:
            for self_parameter in self.parameter_list[url]:
                if self_parameter == parameter:
                    return True
        return False

    def check_unique_parameter(self, parameter: str):
        if not parameter in self.uparameter_list:
            return False
        if self.uparameter_list[parameter] >= 75:
            return False
        return True

class PathFunction:
    def __init__(self):
        pass
    
    def urlerslasher(self, xpath: str) -> str:
        if not xpath:
            return xpath
        ypath = self.slasher(self.urler(xpath))
        return ypath
    
    def slasher(self, xpath: str) -> str:
        if not xpath:
            return xpath + '/'
        if xpath[-1] != '/':
            ypath = xpath + '/'
        else:
            ypath = xpath
        return ypath
    
    def unslasher(self, xpath: str) -> str:
        if not xpath:
            return xpath
        if xpath[-1] == '/':
            ypath = xpath[:-1]
        else:
            ypath = xpath
        return ypath
    
    def questioner(self, xpath: str) -> str:
        if not xpath:
            return xpath + '?'
        if xpath[-1] != '?':
            ypath = xpath + '?'
        else:
            ypath = xpath
        return ypath

    def payloader(self, xpath: str) -> str:
        if not xpath:
            return xpath
        if xpath[0] == '/':
            ypath = xpath[1:]
        else:
            ypath = xpath
        return ypath

    def urler(self, xpath: str) -> str:
        if not xpath:
            return xpath
        if not xpath.startswith('http://') and not xpath.startswith('https://'):
            ypath = "http://" + xpath
        else:
            ypath = xpath
        return ypath

    def unurler(self, xpath: str) -> str:
        if not xpath:
            return xpath
        if not '://' in xpath:
            ypath = xpath
        else:
            ypath = xpath.split('://')[-1]
        return ypath

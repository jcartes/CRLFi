from urllib.parse import urlparse
from lib.PathFunctions import PathFunction
class PathFuzz:
    def __init__(self):
        self.FPathApp = PathFunction()
            
    def FuzzPath(self, unparsed_url: str, payload: str) -> str:
        try:
            half_payload = urlparse(self.FPathApp.slasher(self.FPathApp.urler(unparsed_url)))
            usable_payload = self.FPathApp.payloader(payload)
            full_payload = half_payload.scheme + '://' + half_payload.netloc + half_payload.path + usable_payload
            return full_payload
        except Exception as e:
            print(f"Exception: {e} occured")

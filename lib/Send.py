from requests import Session
from termcolor import colored
from random import randint
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError

from lib.Globals import ColorObj

class Send:
    def __init__(self):
        self.s = Session()
        self.isReturnable = False
        self.error_occured = False

    def deliver_request(self, url):
        r = randint(0, 1)
        self.isReturnable = False
        self.error_occured = False
        error_string = f"{ColorObj.bad} Continuing to next url: Error {E.__class__} occured"
        print(f"{ColorObj.information} Trying {colored(url, color='cyan')} against web server!")
        try:
            if r == 0:
                response = self.s.get(url, timeout=5)
            elif r == 1:
                response = self.s.head(url, timeout=5)
        except ConnectionError:
            print(error_string)
            self.error_occured = True
            return url, False
        except Timeout:
            print(error_string)
            self.error_occured = True
            return url, False
        except Exception as E:
            print(error_string)
            self.error_occured = True
            return url, False
        
        try:
            print(f"{ColorObj.good} Response header: {response.headers['evil-here']}")
            self.isReturnable = True
        except:
            try:
                print(f"{ColorObj.good} Response Cookie: {response.cookies['bugbounty']}")
                self.isReturnable = True
            except:
                pass

    def sender_function(self, url: str) -> tuple:
        self.isReturnable = False
        url, exploitable  = self.deliver_request(url)
        if self.error_occured: return url, exploitable
        if self.isReturnable: return url, exploitable
        instantiated_url = url.replace('http://', 'https://')
        url, exploitable = self.deliver_request(instantiated_url)
        if self.error_occured: return instantiated_url, exploitable
        if self.isReturnable: return instantiated_url, exploitable 
        instantiated_url = url.replace('http://', 'http://www.')
        url, exploitable = self.deliver_request(instantiated_url)
        if self.error_occured: return instantiated_url, exploitable
        if self.isReturnable: return instantiated_url, exploitable

from random import randint
from requests import Session
from termcolor import colored
from traceback import print_exc
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError

from lib.Globals import Color

class Send:
    def __init__(self):
        self.s = Session()
        self.isReturnable = False
        self.error_occured = False

    def deliver_request(self, url):
        r = randint(0, 1)
        self.isReturnable = False
        self.error_occured = False
        error_string = lambda error: f"{Color.bad} Skipping url due to {error}"
        print(f"{Color.information} Trying {colored(url, color='cyan')} against web server!")
        try:
            if r == 0:
                response = self.s.get(url, timeout=5)
            elif r == 1:
                response = self.s.head(url, timeout=5)
        except ConnectionError:
            print(error_string("ConnectionError"))
            self.error_occured = True
            return url, False
        except Timeout:
            print(error_string("TimeoutError"))
            self.error_occured = True
            return url, False
        except Exception as E:
            print(error_string("OtherError"))
            self.error_occured = True
            return url, False
        
        try:
            print(f"{Color.good} Response header: {response.headers['evil-here']}")
            self.isReturnable = True
            return url, True
        except:
            try:
                print(f"{Color.good} Response Cookie: {response.cookies['bugbounty']}")
                self.isReturnable = True
                return url, True
            except:
                return url, False

    def sender_function(self, url: str) -> tuple:
        try:
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
        except Exception as E:
            print_exc()

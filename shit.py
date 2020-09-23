import faster_than_requests
try:
    data = faster_than_requests.get('http://bhphotovideo.com/', timeout = 5000)
    for key in data.keys():
        print(key)
    print(data["version"])
    print(data["status"])
except Exception as E:
    if str(E.__class__) == "<class 'nimpy.OSError'>":
        print("Unrecognized service")
    elif str(E.__class__) == "<class 'nimpy.TimeoutError'>":
        print("Timed out")


# CRLFi
## Description
Semi Automated CRLF injection scanner with concurrency. Scans for CRLF injection in parameters, paths and netlocs.

## Features
1. Automatic scanning of CRLF injection using threads.
2. Define your own payloads in lib/Globals.py.
3. Scans for CRLF injection in parameters, paths and netlocs.
4. Nice UI and automatically skips same looking parameters and paths.

## Usage
```
usage: CRLFi [-h] [-w WORDLIST] [-oD OUTPUT_DIRECTORY] [-d DOMAIN] [-t THREADS] [-b]

CRLFi Finding Tool

optional arguments:
  -h, --help            show this help message and exit
  -w WORDLIST, --wordlist WORDLIST
                        Absolute path of input file
  -oD OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        Output file directory
  -d DOMAIN, --domain DOMAIN
                        Domain name
  -t THREADS, --threads THREADS
                        No of threads
  -b, --banner          Print banner and exit

Enjoy bug hunting
```

## Example
1. Scan a single URL  
* ```CRLFi -d google.com```  
2. Scan URLs from wordlist
* ```CRLFi -w /path/to/wordlist -oD `pwd` -t 10 -d domain.com```  
3. Scan from stdin
* ```assetfinder yahoo.com | CRLFi --- -t 10```


## Caveats
1. Nothing. If you think there is feel free to raise issue.

## FAQ
1. Does CRLF injection only affect HTTP/1?  
* Well, no. I found CRLF injection on 2 http/2 enabled website with http2. Also checkout this: [CRLF injection in HTTP2](https://security.stackexchange.com/questions/235046/does-http-2-prevent-security-vulnerabilites-like-crlf-injection)

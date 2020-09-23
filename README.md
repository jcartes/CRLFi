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
Scan a single URLs  
* ```CRLFi -w <(echo 'google.com') -oD `pwd` -t 1 -d google.com```  
Scan from URLs  
* ```CRLFi -w /tmp/files.txt -oD `pwd` -t 10 -d anydomainnameinfiles.txt.com```  

## Caveats
1. Nothing. If you think there is feel free to raise issue.

## FAQ
1. Does CRLF injection only affect HTTP/1?  
<<<<<<< HEAD
* Well, no. I found CRLF injection on 2 different HTTP/2 enabled website using this tool and confirmed with curl with `--http2` in curl. Also my question: [CRLF injection in HTTP2](https://security.stackexchange.com/questions/235046/does-http-2-prevent-security-vulnerabilites-like-crlf-injection)
=======
* Well, no. I found CRLF injection on 2 http/2 enabled website with http2. Also checkout this: [CRLF injection in HTTP2](https://security.stackexchange.com/questions/235046/does-http-2-prevent-security-vulnerabilites-like-crlf-injection)
>>>>>>> parent of 00220c8... 11:56:37 PM 09/12/2020

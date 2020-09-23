def starter(argv):
    if not argv.domain:
        if not argv.wordlist or not argv.output_directory:
            if not argv.stdin:
                print("{} Use --help".format(ColorObj.bad))
                exit()
            else:
                stdinarray = stdin.read().split('\n')
                return [line.rstrip('\n').strip(' ') for line in stdinarray if line]
        else:
            return [line.rstrip('\n') for line in open(argv.wordlist) if line]
    else:
        return [argv.domain.strip(' ')]

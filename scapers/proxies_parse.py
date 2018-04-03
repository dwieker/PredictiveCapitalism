from sys import argv
import re

fp=argv[1]

with open(fp, 'r') as f:
    proxies = f.readlines()

proxies = [re.search( r'[0-9]+(?:\.[0-9]+){3}:[0-9][0-9][0-9][0-9]', s).group() + '\n' for s in proxies]
print(proxies)

with open('proxies_parsed.txt', 'w') as f:
	f.writelines(proxies)

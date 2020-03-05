#!/usr/bin/env python3

import sys
import json
import tabulate


if sys.stdin.isatty():
        print('missing piped data')
        sys.exit(1)

data = json.loads(sys.stdin.read())

print(tabulate.tabulate(data, headers='keys'))

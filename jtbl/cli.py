#!/usr/bin/env python3

import sys
import json
import tabulate


if sys.stdin.isatty():
        print('missing piped data')
        sys.exit(1)

data = json.loads(sys.stdin.read())

# wrap every 15 chars for all field values
for entry in data:
    for k, v in entry.items():
        if v is not None:
            entry[k] = '\n'.join([str(v)[i:i + 15] for i in range(0, len(str(v)), 15)])

print(tabulate.tabulate(data, headers='keys'))

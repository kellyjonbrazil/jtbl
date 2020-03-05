#!/usr/bin/env python3

import sys
import json
import tabulate


def main():
    if sys.stdin.isatty():
            print('missing piped data')
            sys.exit(1)

    data = json.loads(sys.stdin.read())

    # auto 'slurp' data if it is not already a list of dictionaries
    if type(data) is not list:
        data_list = []
        data_list.append(data)
        data = data_list

    # wrap every 17 chars for all field values
    for entry in data:
        for k, v in entry.items():
            if v is not None:
                entry[k] = '\n'.join([str(v)[i:i + 17] for i in range(0, len(str(v)), 17)])

    print(tabulate.tabulate(data, headers='keys'))


if __name__ == '__main__':
    main()

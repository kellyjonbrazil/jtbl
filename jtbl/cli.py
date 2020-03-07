#!/usr/bin/env python3

import sys
import json
import tabulate
import shutil


def main():
    table_format = 'simple'
    columns = shutil.get_terminal_size().columns

    if sys.stdin.isatty():
            print('jtbl:  Missing piped data\n')
            sys.exit(1)

    pipe_data = sys.stdin.read()

    try:
        data = json.loads(pipe_data)
        if type(data) is not list:
            data_list = []
            data_list.append(data)
            data = data_list

    except Exception:
        # if json.loads fails, assume the data is formatted as json lines and parse
        data = pipe_data.splitlines()
        data_list = []
        for jsonline in data:
            try:
                entry = json.loads(jsonline)
                data_list.append(entry)
            except Exception as e:
                # can't parse the data. Throw a nice message and quit
                print(f'jtbl:  Exception - {e}\n       Can not parse the following line (Not JSON or JSON Lines data):\n       {jsonline[0:74]}\n', file=sys.stderr)
                sys.exit(1)

        data = data_list

    # find the length of the keys (headers) and longest values
    data_width = {}
    for entry in data:
        for k, v in entry.items():
            if k in data_width:
                if len(str(v)) > data_width[k]:
                    data_width[k] = len(str(v))
            else:
                data_width[k] = len(str(v))

    # header_width and value_width calculations are only approximate since there can be left and right justification
    num_of_headers = len(data_width.keys())
    combined_total_list = []
    for k, v in data_width.items():
        highest_value = max(len(k) + 4, v)
        combined_total_list.append(highest_value)

    total_width = sum(combined_total_list) + 4

    if total_width > columns:
        table_format = 'grid'
        wrap_width = int(columns / num_of_headers)

        # wrap every wrap_width chars for all field values
        for entry in data:
            for k, v in entry.items():
                if v is not None:
                    entry[k] = '\n'.join([str(v)[i:i + wrap_width] for i in range(0, len(str(v)), wrap_width)])

    print(tabulate.tabulate(data, headers='keys', tablefmt=table_format))


if __name__ == '__main__':
    main()

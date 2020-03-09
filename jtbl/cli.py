#!/usr/bin/env python3

import sys
import signal
import json
import tabulate
import shutil

__version__ = '0.5.0'


def ctrlc(signum, frame):
    """exit with error on SIGINT"""
    sys.exit(1)


def main():
    # break on ctrl-c keyboard interrupt
    signal.signal(signal.SIGINT, ctrlc)

    options = []

    # options
    for opt in sys.argv:
        if opt.startswith('-') and not opt.startswith('--'):
            options.extend(opt[1:])

    version_info = 'v' in options
    helpme = 'h' in options
    truncate = 't' in options

    if version_info:
        print(f'jtbl:   version {__version__}\n')
        exit()

    if helpme:
        print('jtbl:   Converts JSON and JSON Lines to a table\n\nUsage:  <JSON Data> | jtbl [OPTIONS]\n\n        -t  truncate data instead of wrapping if too long for the terminal width\n        -v  version info\n        -h  help\n')
        exit()

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
        try:
            for k, v in entry.items():
                if k in data_width:
                    if len(str(v)) > data_width[k]:
                        data_width[k] = len(str(v))
                else:
                    data_width[k] = len(str(v))
        except Exception:
            # can't parse the data. Throw a nice message and quit
            if not entry:
                entry = '<null data>'

            print(f'jtbl:  Can not represent this part of the JSON Object.\n       (Could be an Array or null data instead of an Object):\n       {entry[0:74]}\n', file=sys.stderr)
            sys.exit(1)

    # highest_value calculations are only approximate since there can be left and right justification
    num_of_headers = len(data_width.keys())
    combined_total_list = []
    for k, v in data_width.items():
        highest_value = max(len(k) + 4, v + 2)
        combined_total_list.append(highest_value)

    total_width = sum(combined_total_list)

    if total_width > columns:
        # Find the best wrap_width based on the terminal size
        sorted_list = sorted(combined_total_list, reverse=True)
        wrap_width = sorted_list[0]

        scale = 4.5
        if truncate:
            scale = 2

        while wrap_width > 4 and total_width >= (columns - (num_of_headers * scale)):
            sorted_list = sorted(sorted_list, reverse=True)
            sorted_list[0] -= 1
            total_width = sum(sorted_list)
            wrap_width = sorted_list[0]

        # truncate or wrap every wrap_width chars for all field values
        for entry in data:
            delete_keys = []
            add_keys = []
            for k, v in entry.items():
                if v is not None:
                    if truncate:
                        new_key = str(k)[0:wrap_width]
                        new_value = str(v)[0:wrap_width]
                        if k != new_key or v != new_value:
                            delete_keys.append(k)
                            add_keys.append((new_key, new_value))

                    else:
                        table_format = 'grid'
                        new_key = '\n'.join([str(k)[i:i + wrap_width] for i in range(0, len(str(k)), wrap_width)])
                        new_value = '\n'.join([str(v)[i:i + wrap_width] for i in range(0, len(str(v)), wrap_width)])
                        if k != new_key or v != new_value:
                            delete_keys.append(k)
                            add_keys.append((new_key, new_value))

            for i in delete_keys:
                del entry[i]

            for i in add_keys:
                entry[i[0]] = i[1]

    print(tabulate.tabulate(data, headers='keys', tablefmt=table_format))


if __name__ == '__main__':
    main()

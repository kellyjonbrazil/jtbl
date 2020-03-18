#!/usr/bin/env python3

import sys
import signal
import json
import tabulate
import shutil

__version__ = '1.0.0'


def ctrlc(signum, frame):
    """exit with error on SIGINT"""
    sys.exit(1)


def get_stdin():
    if sys.stdin.isatty():
        return None

    return sys.stdin.read()


def print_error(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def wrap(data, columns, table_format, truncate):
    """wrap or truncate the data to fit the terminal width"""

    # find the length of the keys (headers) and longest values
    data_width = {}
    for entry in data:
        for k, v in entry.items():
            if k in data_width:
                if len(str(v)) > data_width[k]:
                    data_width[k] = len(str(v))
            else:
                data_width[k] = len(str(v))

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
        scale = 2.5 if truncate else 4.5

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
                if v is None:
                    v = ''

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

    return (data, table_format)


def make_table(pipe_data=None, args='', columns=None, table_format='simple'):
    if columns is None:
        columns = shutil.get_terminal_size().columns

    # break on ctrl-c keyboard interrupt
    signal.signal(signal.SIGINT, ctrlc)

    options = []
    for arg in args:
        if arg.startswith('-') and not arg.startswith('--'):
            options.extend(arg[1:])

    nowrap = 'n' in options
    truncate = 't' in options
    version_info = 'v' in options
    helpme = 'h' in options

    if version_info:
        return (False, f'jtbl:   version {__version__}\n')

    if helpme:
        return (False, 'jtbl:   Converts JSON and JSON Lines to a table\n\nUsage:  <JSON Data> | jtbl [OPTIONS]\n\n        -n  do not try to wrap if too long for the terminal width\n        -t  truncate data instead of wrapping if too long for the terminal width\n        -v  version info\n        -h  help\n')

    if pipe_data is None:
        return (True, 'jtbl:  Missing piped data\n')

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
        for i, jsonline in enumerate(data):
            try:
                entry = json.loads(jsonline)
                data_list.append(entry)
            except Exception as e:
                # can't parse the data. Throw a nice message and quit
                return (True, f'jtbl:  Exception - {e}\n       Cannot parse line {i + 1} (Not JSON or JSON Lines data):\n       {str(jsonline)[0:columns - 8]}\n')

        data = data_list

    try:
        if not isinstance(data[0], dict):
            data = json.dumps(data)
            return (True, f'jtbl:  Cannot represent this part of the JSON Object as a table.\n       (Could be an Element, an Array, or Null data instead of an Object):\n       {str(data)[0:columns - 8]}\n')

    except Exception:
        # can't parse the data. Throw a nice message and quit
        return (True, f'jtbl:  Cannot parse the data (Not JSON or JSON Lines data):\n       {str(data)[0:columns - 8]}\n')

    if not nowrap:
        data, table_format = wrap(data=data, columns=columns, table_format=table_format, truncate=truncate)

    return (False, tabulate.tabulate(data, headers='keys', tablefmt=table_format))


def main():
    error = False
    stdin = get_stdin()
    error, result = make_table(pipe_data=stdin, args=sys.argv)

    if error:
        print_error(result)
    else:
        print(result)


if __name__ == '__main__':
    main()
